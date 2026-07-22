// supabase/functions/live-sync-recordings/index.ts
// Sincroniza grabaciones publicadas de BBB → sesiones_vivo + lecciones (tipo link/vivo).
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-sync-secret",
};

async function sha1(message: string): Promise<string> {
  const buf = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(message));
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function apiBase(bbbUrl: string): string {
  let base = bbbUrl.trim().replace(/\/+$/, "");
  if (!base.includes("bigbluebutton")) base += "/bigbluebutton";
  if (!base.endsWith("/api")) base += "/api";
  return base + "/";
}

function encodeParams(params: Record<string, string>): string {
  return Object.keys(params)
    .map((k) => {
      const key = encodeURIComponent(k).replace(/%20/g, "+");
      const val = encodeURIComponent(params[k]).replace(/%20/g, "+");
      return `${key}=${val}`;
    })
    .join("&");
}

function xmlTag(xml: string, tag: string): string {
  const m = xml.match(
    new RegExp(`<${tag}><!\\[CDATA\\[([\\s\\S]*?)\\]\\]><\\/${tag}>|<${tag}>([\\s\\S]*?)<\\/${tag}>`),
  );
  return (m?.[1] ?? m?.[2] ?? "").trim();
}

function xmlBlocks(xml: string, tag: string): string[] {
  const re = new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, "g");
  const out: string[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(xml)) !== null) out.push(m[1]);
  return out;
}

type Rec = {
  recording_id: string;
  meeting_id: string;
  name: string;
  published: boolean;
  playback_url: string;
};

async function getRecordings(base: string, secret: string, meetingId?: string): Promise<Rec[]> {
  const params: Record<string, string> = {};
  if (meetingId) params.meetingID = meetingId;
  const qs = encodeParams(params);
  const checksum = await sha1(`getRecordings${qs}${secret}`);
  const url = `${apiBase(base)}getRecordings?${qs}${qs ? "&" : ""}checksum=${checksum}`;
  const res = await fetch(url);
  const text = await res.text();
  if (xmlTag(text, "returncode") !== "SUCCESS") {
    throw new Error(xmlTag(text, "message") || "getRecordings failed");
  }
  const out: Rec[] = [];
  for (const block of xmlBlocks(text, "recording")) {
    const recording_id = xmlTag(`<recording>${block}</recording>`, "recordID");
    const meeting_id = xmlTag(`<recording>${block}</recording>`, "meetingID");
    const name = xmlTag(`<recording>${block}</recording>`, "name");
    const published = xmlTag(`<recording>${block}</recording>`, "published").toLowerCase() === "true";
    const playback_url = xmlTag(`<recording>${block}</recording>`, "url");
    if (recording_id) {
      out.push({ recording_id, meeting_id, name, published, playback_url });
    }
  }
  return out;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const syncSecret = Deno.env.get("SYNC_CRON_SECRET") || "";
    const headerSecret = req.headers.get("X-Sync-Secret") || "";
    const auth = req.headers.get("Authorization") || "";
    const bearer = auth.startsWith("Bearer ") ? auth.slice(7) : "";

    if (syncSecret && headerSecret !== syncSecret && bearer !== syncSecret) {
      return new Response(JSON.stringify({ error: "No autorizado" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const BBB_URL = Deno.env.get("BBB_URL") || "";
    const BBB_SECRET = Deno.env.get("BBB_SECRET") || "";
    const SUPABASE_URL = Deno.env.get("SUPABASE_URL") || "";
    const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";

    if (!BBB_URL || !BBB_SECRET) {
      return new Response(JSON.stringify({ error: "BBB no configurado" }), {
        status: 503,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE);
    const { data: sesiones, error } = await admin
      .from("sesiones_vivo")
      .select("id, curso_id, titulo, bbb_meeting_id, recording_id")
      .not("bbb_meeting_id", "is", null);

    if (error) throw error;

    let updated = 0;
    let lessons = 0;

    for (const sesion of sesiones || []) {
      const recs = await getRecordings(BBB_URL, BBB_SECRET, sesion.bbb_meeting_id);
      const published = recs.filter((r) => r.published && r.playback_url);
      if (!published.length) continue;

      // Preferir la más reciente (última en lista)
      const rec = published[published.length - 1];
      if (sesion.recording_id === rec.recording_id) continue;

      await admin
        .from("sesiones_vivo")
        .update({
          recording_url: rec.playback_url,
          recording_id: rec.recording_id,
          estado: "finalizada",
        })
        .eq("id", sesion.id);
      updated += 1;

      const { data: existing } = await admin
        .from("lecciones")
        .select("id")
        .eq("bbb_recording_id", rec.recording_id)
        .maybeSingle();

      if (!existing) {
        const { data: maxOrden } = await admin
          .from("lecciones")
          .select("orden")
          .eq("curso_id", sesion.curso_id)
          .order("orden", { ascending: false })
          .limit(1)
          .maybeSingle();
        const orden = (maxOrden?.orden || 0) + 1;
        await admin.from("lecciones").insert({
          curso_id: sesion.curso_id,
          titulo: `Grabación: ${sesion.titulo || rec.name || "Clase en vivo"}`,
          orden,
          tipo: "vivo",
          contenido: rec.playback_url,
          bbb_recording_id: rec.recording_id,
        });
        lessons += 1;
      }
    }

    return new Response(JSON.stringify({ ok: true, sesiones_actualizadas: updated, lecciones_creadas: lessons }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
