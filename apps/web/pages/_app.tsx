import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import { SessionProvider } from 'next-auth/react';

// Global application component.  Wraps all pages with the SessionProvider to
// enable authentication.  To enable Google login, configure next-auth in
// pages/api/auth/[...nextauth].ts and provide your Google OAuth credentials.

export default function App({ Component, pageProps: { session, ...pageProps } }: AppProps) {
  return (
    <SessionProvider session={session}>
      <Component {...pageProps} />
    </SessionProvider>
  );
}
