import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

// This API route enables authentication via Google.  To use it, create
// a Google OAuth client in the Google Developers Console and set the
// environment variables GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your
// deployment environment.

export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
});
