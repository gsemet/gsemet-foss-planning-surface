import React from "react";
import { AbsoluteFill, Composition, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import take from "./take.json";

// Trial of the storyboard panels 1, 2, 3, 6 and 7: real VS Code footage on the green identity.
const FPS = 30;
const C = { teal: "#0d5360", tealDark: "#082f37", tealLight: "#11707f", orange: "#f2822b", accent: "#ffb06a", pale: "#d6ebee" };
const FONT = `-apple-system, "SF Pro Display", "Helvetica Neue", Inter, Arial, sans-serif`;
const WIN = { x: 160, y: 34, w: 1600, h: 900 };
const CARD = 36;
const FADE = 9;

type Shot = { from: number; to: number; caption: string; callout?: { text: string; at: number; x: number; y: number }; zoom?: boolean };
const p = take.panels as Record<string, number>;
const click = take.clicks;
const SHOTS: Shot[] = [
  { from: p["2"] + 0.5, to: p["3"] + 0.25, caption: "Your **agent** writes Markdown" },
  { from: p["3"] + 1.2, to: p["3"] + 4.2, caption: "**You** get a real page", callout: { text: "No configuration", at: 0.7, x: 1010, y: 210 } },
  { from: p["6"] + 0.5, to: click[1].t + 2.0, caption: "**Answer** your agent", zoom: true, callout: { text: "Saved in the file", at: click[1].t - (p["6"] + 0.5) + 0.35, x: 190, y: 470 } },
];
const lengths = SHOTS.map((s) => Math.round((s.to - s.from) * FPS));
const starts = lengths.reduce<number[]>((a, l, i) => [...a, i === 0 ? CARD : a[i - 1] + lengths[i - 1] - FADE], []);
const STAGE_END = starts.at(-1)! + lengths.at(-1)!;
const END_CARD = 69;
export const TOTAL = STAGE_END + END_CARD - FADE;

const Accented: React.FC<{ text: string; base?: string; delay?: number }> = ({ text, base = "#fff", delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  let on = false;
  const words = text.split(" ").map((raw) => {
    const open = raw.startsWith("**"), close = raw.endsWith("**");
    if (open) on = true;
    const w = { t: raw.replaceAll("**", ""), accent: on };
    if (close) on = false;
    return w;
  });
  return <>{words.map((w, i) => {
    const s = spring({ frame: frame - delay - i * 2, fps, config: { damping: 18, stiffness: 170 } });
    return <span key={i} style={{ display: "inline-block", marginRight: "0.26em", opacity: s, transform: `translateY(${(1 - s) * 18}px)`, color: w.accent ? C.accent : base }}>{w.t}</span>;
  })}</>;
};

const Green: React.FC<{ children?: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: `radial-gradient(1200px 800px at 70% 20%, ${C.tealLight} 0%, ${C.teal} 38%, ${C.tealDark} 100%)` }}>{children}</AbsoluteFill>
);

const Card: React.FC<{ subtitle: string; link?: string; extra?: string }> = ({ subtitle, link, extra }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 16 } });
  const line = interpolate(frame, [6, 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Green>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", fontFamily: FONT, gap: 26 }}>
        <Img src={staticFile("logo.png")} style={{ width: 170, borderRadius: 85, opacity: pop, transform: `scale(${0.85 + 0.15 * pop})` }} />
        <div style={{ fontSize: 96, fontWeight: 700, letterSpacing: -1.2 }}><Accented text="Markdown OKF Schema **Studio**" delay={2} /></div>
        <div style={{ width: 520 * line, height: 5, background: C.orange, borderRadius: 3 }} />
        <div style={{ fontSize: 42, fontWeight: 500 }}><Accented text={subtitle} base={C.pale} delay={8} /></div>
        {link ? <div style={{ fontFamily: `"SF Mono", Menlo, monospace`, fontSize: 28, color: "#fff", background: "rgba(0,0,0,0.3)", border: `2px solid ${C.orange}`, padding: "12px 28px", borderRadius: 14, opacity: line }}>{link}</div> : null}
        {extra ? <div style={{ fontSize: 42, fontWeight: 700, color: C.orange, opacity: line }}>{extra}</div> : null}
      </AbsoluteFill>
    </Green>
  );
};

const lerpTrack = (t: number) => {
  const m = take.mouse;
  if (t <= m[0].t) return m[0];
  for (let i = 1; i < m.length; i++) if (m[i].t >= t) {
    const k = (t - m[i - 1].t) / Math.max(1e-3, m[i].t - m[i - 1].t);
    return { x: m[i - 1].x + (m[i].x - m[i - 1].x) * k, y: m[i - 1].y + (m[i].y - m[i - 1].y) * k };
  }
  return m[m.length - 1];
};

const Window: React.FC<{ shot: Shot; length: number }> = ({ shot, length }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = shot.from + frame / fps;
  const [cw, ch] = take.size;
  const k = WIN.w / cw;
  let scale = 1, ox = 0, oy = 0;
  if (shot.zoom) {
    const r = take.zoom;
    const target = Math.min(1.4, cw / r.w, ch / r.h);
    const z = interpolate(frame, [4, 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
    scale = 1 + (target - 1) * z;
    const cx = (r.x + r.w / 2) * k, cy = (r.y + r.h / 2) * k;
    ox = (WIN.w / 2 - cx * target) * z;
    oy = (WIN.h / 2 - cy * target) * z;
    ox = Math.min(0, Math.max(WIN.w - WIN.w * scale, ox));
    oy = Math.min(0, Math.max(WIN.h - WIN.h * scale, oy));
  }
  const m = lerpTrack(t);
  const ripple = take.clicks.map((c) => (t - c.t) / 0.45).find((v) => v >= 0 && v < 1);
  const c = shot.callout;
  const cs = c ? spring({ frame: frame - c.at * fps, fps, config: { damping: 15 } }) : 0;
  return (
    <>
      <div style={{ position: "absolute", left: WIN.x, top: WIN.y, width: WIN.w, height: WIN.h, borderRadius: 16, overflow: "hidden", boxShadow: "0 30px 70px rgba(0,0,0,0.45)", background: "#fff" }}>
        <div style={{ position: "absolute", width: WIN.w, height: WIN.h, transformOrigin: "0 0", transform: `translate(${ox}px, ${oy}px) scale(${scale})` }}>
          <OffthreadVideo src={staticFile("clip.mp4")} startFrom={Math.round(shot.from * fps)} muted style={{ width: WIN.w, height: WIN.h, objectFit: "cover", objectPosition: "top" }} />
          {ripple !== undefined ? <div style={{ position: "absolute", left: m.x * k - 34, top: m.y * k - 34, width: 68, height: 68, borderRadius: 34, border: `4px solid ${C.orange}`, opacity: 1 - ripple, transform: `scale(${0.4 + ripple})` }} /> : null}
          <svg style={{ position: "absolute", left: m.x * k - 4, top: m.y * k - 3, width: 34, height: 44 }} viewBox="0 0 20 25"><path d="M3 2 L3 18.5 L7.4 14.6 L10.2 21 L12.9 19.8 L10.1 13.5 L16 13.2 Z" fill="#fff" stroke="#111" strokeWidth="1.5" strokeLinejoin="round" /></svg>
        </div>
        {c ? <div style={{ position: "absolute", left: c.x, top: c.y, opacity: cs, transform: `scale(${0.9 + 0.1 * cs})`, fontFamily: FONT, fontSize: 34, fontWeight: 700, color: "#fff", background: C.teal, padding: "12px 26px", borderRadius: 30, boxShadow: "0 10px 26px rgba(0,0,0,0.3)" }}>{c.text}</div> : null}
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: WIN.y + WIN.h + 28, textAlign: "center", fontFamily: FONT, fontSize: 56, fontWeight: 600, opacity: interpolate(frame, [length - FADE - 3, length - FADE], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>
        <Accented text={shot.caption} delay={FADE} />
      </div>
    </>
  );
};

const Fade: React.FC<{ length: number; first?: boolean; children: React.ReactNode }> = ({ length, first, children }) => {
  const frame = useCurrentFrame();
  const o = first ? 1 : interpolate(frame, [0, FADE], [0, 1], { extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

const Trial: React.FC = () => (
  <AbsoluteFill>
    <Green />
    <Sequence durationInFrames={CARD + FADE}><Card subtitle="Read, review and edit rich Markdown in one page" /></Sequence>
    {SHOTS.map((s, i) => (
      <Sequence key={i} from={starts[i]} durationInFrames={lengths[i]}>
        <Fade length={lengths[i]}><Green /><Window shot={s} length={lengths[i]} /></Fade>
      </Sequence>
    ))}
    <Sequence from={STAGE_END - FADE}><Fade length={END_CARD}><Card subtitle="Free on the VS Code Marketplace" link="marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio" extra="Works with your coding agent" /></Fade></Sequence>
  </AbsoluteFill>
);

export const Root: React.FC = () => <Composition id="Trial" component={Trial} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080} />;
