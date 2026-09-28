"use client";
/**
 * <LiquidGlass> — React / Next.js wrapper for liquid-glass.js
 * 1. Copy liquid-glass.js to /public/liquid-glass.js
 * 2. Import tokens.css once (e.g. in app/layout.tsx)
 * 3. <LiquidGlass className="p-6" options={{ scale: -80 }}>...</LiquidGlass>
 * Chromium gets real refraction; Safari/Firefox get the frosted fallback.
 */
import { useEffect, useRef, type CSSProperties, type ReactNode } from "react";

type GlassOptions = {
  scale?: number; chroma?: number; border?: number; mapBlur?: number;
  blur?: number; saturate?: number; radius?: number | null; fallbackBlur?: number;
};
type GlassHandle = { supported: boolean; refresh: () => void; destroy: () => void };

declare global {
  interface Window { liquidGlass?: (el: HTMLElement, o?: GlassOptions) => GlassHandle }
}

let loader: Promise<void> | null = null;
function loadModule(src: string): Promise<void> {
  if (typeof window === "undefined") return Promise.resolve();
  if (window.liquidGlass) return Promise.resolve();
  if (!loader) {
    loader = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src; s.async = true;
      s.onload = () => resolve();
      s.onerror = () => { loader = null; reject(new Error("liquid-glass.js failed to load")); };
      document.head.appendChild(s);
    });
  }
  return loader;
}

export function LiquidGlass({
  children, className = "", style, options, src = "/liquid-glass.js", as: Tag = "div",
}: {
  children?: ReactNode; className?: string; style?: CSSProperties;
  options?: GlassOptions; src?: string; as?: "div" | "nav" | "section" | "aside" | "header";
}) {
  const ref = useRef<HTMLElement | null>(null);
  const optsKey = JSON.stringify(options ?? {});

  useEffect(() => {
    let handle: GlassHandle | null = null;
    let cancelled = false;
    // Respect reduced transparency: keep the solid CSS fallback, skip refraction.
    if (window.matchMedia?.("(prefers-reduced-transparency: reduce)").matches) return;
    loadModule(src)
      .then(() => {
        if (!cancelled && ref.current && window.liquidGlass) {
          handle = window.liquidGlass(ref.current, options);
        }
      })
      .catch(() => { /* frosted CSS fallback stays in place */ });
    return () => { cancelled = true; handle?.destroy(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [src, optsKey]);

  return (
    <Tag ref={ref as never} className={`lg-glass lg-refract ${className}`} style={style}>
      {children}
    </Tag>
  );
}

export default LiquidGlass;
