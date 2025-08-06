# 🚀 FLYFOX AI - Vercel Deployment Guide

## **Framework Preset Configuration**

Your FLYFOX AI platform uses **Vite + React**, which requires the following Vercel configuration:

### **Framework Preset: `vite`**
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`
- **Dev Command**: `npm run dev`

## **Prerequisites**

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in `GoliathBritton/flyfox-ai-platform`
3. **Domain**: `flyfoxai.com` (already configured)

## **Deployment Steps**

### **Step 1: Connect to Vercel**

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository: `GoliathBritton/flyfox-ai-platform`
4. Vercel will automatically detect it's a **Vite** project

### **Step 2: Configure Environment Variables**

In your Vercel project settings, add these environment variables:

```
VITE_SUPABASE_URL=https://hysfiibfajydjatsqtbz.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5c2ZpaWJmYWp5ZGphdHNxdGJ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0NjQzNjMsImV4cCI6MjA3MDA0MDM2M30.7bwhYLgCkHSlQXc14NuCpOY6y4jd8MjMc8zOIqynGjE
VITE_WEBSITE_URL=https://flyfoxai.com
VITE_APP_URL=https://app.flyfoxai.com
VITE_API_URL=https://api.flyfoxai.com
VITE_VOICE_URL=https://voice.flyfoxai.com
VITE_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key_here
VITE_PAYPAL_CLIENT_ID=ARbHoAvcE25ruW5AoK414FTnkW_ufJWWiPwPgHyyU7ypOyDLIRKvNpoaEOGyV4j8U6Wxvtk-3OjA-LxK
```

### **Step 3: Configure Custom Domain**

1. In Vercel project settings, go to "Domains"
2. Add your custom domain: `app.flyfoxai.com`
3. Update your DNS records as per `FLYFOX_AI_DNS_CONFIGURATION_GUIDE.md`

### **Step 4: Deploy**

1. Vercel will automatically build and deploy your app
2. The build process will:
   - Install dependencies (`npm install`)
   - Build the React app (`npm run build`)
   - Output to `dist` directory
   - Deploy to Vercel's CDN

## **Build Configuration**

Your `vercel.json` is already configured with:

```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

## **Expected Deployment URL**

- **Production**: `https://app.flyfoxai.com`
- **Preview**: `https://flyfox-ai-platform-git-main-goliathbritton.vercel.app`

## **Post-Deployment**

1. **Test the deployment**: Visit `https://app.flyfoxai.com`
2. **Verify environment variables**: Check that Supabase and payment integrations work
3. **Monitor performance**: Use Vercel Analytics to track performance

## **Troubleshooting**

### **Build Failures**
- Check that all dependencies are in `package.json`
- Verify TypeScript compilation passes locally
- Check Vercel build logs for specific errors

### **Environment Variables**
- Ensure all `VITE_*` variables are set in Vercel
- Redeploy after adding new environment variables

### **Domain Issues**
- Verify DNS records are updated correctly
- Allow 24-48 hours for DNS propagation

## **Next Steps**

After successful Vercel deployment:

1. **Test all features**: Voice calling, payment processing, customer management
2. **Set up monitoring**: Vercel Analytics and error tracking
3. **Configure backups**: Database backups and file storage
4. **Launch marketing**: Begin your marketing campaigns

---

**Status**: ✅ Ready for Vercel deployment with Vite framework preset
