// supabase/functions/live-join/index.ts
// Genera URL de join BBB solo si el alumno está inscrito en el curso.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
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
  // BBB espera application/x-www-form-urlencoded (espacios como +)
  return Object.keys(params)
    .map((k) => {
      const key = encodeURIComponent(k).replace(/%20/g, "+");
      const val = encodeURIComponent(params[k]).replace(/%20/g, "+");
      return `${key}=${val}`;
    })
    .join("&");
}

async function bbbBuildUrl(
  apiCall: string,
  params: Record<string, string>,
  secret: string,
  base: string,
): Promise<string> {
  const qs = encodeParams(params);
  const checksum = await sha1(`${apiCall}${qs}${secret}`);
  return `${apiBase(base)}${apiCall}?${qs}&checksum=${checksum}`;
}

function xmlTag(xml: string, tag: string): string {
  const m = xml.match(new RegExp(`<${tag}><!\\[CDATA\\[([\\s\\S]*?)\\]\\]><\\/${tag}>|<${tag}>([\\s\\S]*?)<\\/${tag}>`));
  return (m?.[1] ?? m?.[2] ?? "").trim();
}

async function bbbCall(
  apiCall: string,
  params: Record<string, string>,
  secret: string,
  base: string,
): Promise<string> {
  const url = await bbbBuildUrl(apiCall, params, secret, base);
  const res = await fetch(url);
  const text = await res.text();
  if (xmlTag(text, "returncode") !== "SUCCESS") {
    throw new Error(xmlTag(text, "message") || xmlTag(text, "messageKey") || "BBB error");
  }
  return text;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const BBB_URL = Deno.env.get("BBB_URL") || "";
    const BBB_SECRET = Deno.env.get("BBB_SECRET") || "";
    const SUPABASE_URL = Deno.env.get("SUPABASE_URL") || "";
    const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
    const ANON = Deno.env.get("SUPABASE_ANON_KEY") || "";

    if (!BBB_URL || !BBB_SECRET) {
      return new Response(JSON.stringify({ error: "BBB no configurado (BBB_URL / BBB_SECRET)" }), {
        status: 503,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const authHeader = req.headers.get("Authorization") || "";
    const userClient = createClient(SUPABASE_URL, ANON, {
      global: { headers: { Authorization: authHeader } },
    });
    const admin = createClient(SUPABASE_URL, SERVICE_ROLE);

    const { data: userData, error: userErr } = await userClient.auth.getUser();
    if (userErr || !userData?.user) {
      return new Response(JSON.stringify({ error: "No autenticado" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
    const user = userData.user;

    const body = await req.json().catch(() => ({}));
    const sesionId = String(body.sesion_id || body.sesionId || "").trim();
    const cursoId = String(body.curso_id || body.cursoId || "").trim();
    const asModerator = Boolean(body.as_moderator);

    let sesion: Record<string, unknown> | null = null;

    if (sesionId) {
      const { data, error } = await admin.from("sesiones_vivo").select("*").eq("id", sesionId).maybeSingle();
      if (error) throw error;
      sesion = data;
    } else if (cursoId) {
      const { data, error } = await admin
        .from("sesiones_vivo")
        .select("*")
        .eq("curso_id", cursoId)
        .in("estado", ["programada", "en_vivo"])
        .order("starts_at", { ascending: true })
        .limit(1)
        .maybeSingle();
      if (error) throw error;
      sesion = data;
    }

    if (!sesion) {
      return new Response(JSON.stringify({ error: "No hay sesión en vivo disponible" }), {
        status: 404,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const curso = String(sesion.curso_id);
    const { data: insc, error: inscErr } = await admin
      .from("inscripciones")
      .select("id")
      .eq("user_id", user.id)
      .eq("curso_id", curso)
      .eq("estado", "activo")
      .maybeSingle();
    if (inscErr) throw inscErr;

    const { data: profile } = await admin.from("profiles").select("role, full_name").eq("id", user.id).maybeSingle();
    const isAdmin = profile?.role === "admin";

    if (!insc && !isAdmin) {
      return new Response(JSON.stringify({ error: "No estás inscrito en este curso" }), {
        status: 403,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const meetingId = String(sesion.bbb_meeting_id);
    const attendeePw = String(sesion.attendee_pw || "ap");
    const moderatorPw = String(sesion.moderator_pw || "mp");
    const record = sesion.record !== false;
    const title = String(sesion.titulo || "Clase Metabolic");

    await bbbCall(
      "create",
      {
        name: title,
        meetingID: meetingId,
        attendeePW: attendeePw,
        moderatorPW: moderatorPw,
        record: record ? "true" : "false",
        autoStartRecording: record ? "true" : "false",
        allowStartStopRecording: "true",
        welcome: "Bienvenido a Metabolic Academy",
      },
      BBB_SECRET,
      BBB_URL,
    );

    await admin.from("sesiones_vivo").update({ estado: "en_vivo" }).eq("id", sesion.id);

    const fullName =
      (profile?.full_name && String(profile.full_name).trim()) ||
      user.user_metadata?.full_name ||
      user.email ||
      "Alumno";
    const password = asModerator && isAdmin ? moderatorPw : attendeePw;
    const join = await bbbBuildUrl(
      "join",
      {
        fullName: String(fullName),
        meetingID: meetingId,
        password,
        redirect: "true",
        userID: user.id,
      },
      BBB_SECRET,
      BBB_URL,
    );

    return new Response(JSON.stringify({ url: join, sesion_id: sesion.id, meeting_id: meetingId }), {
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
