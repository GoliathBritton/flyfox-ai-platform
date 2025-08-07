# ✅ FLYFOX AI - Vercel Deployment Checklist

## **Framework Configuration**
- ✅ **Framework Preset**: `vite`
- ✅ **Build Command**: `npm run build`
- ✅ **Output Directory**: `dist`
- ✅ **Install Command**: `npm install`
- ✅ **Dev Command**: `npm run dev`

## **Pre-Deployment Checklist**

### **1. GitHub Repository**
- [ ] Repository exists: `GoliathBritton/flyfox-ai-platform`
- [ ] All code is committed and pushed
- [ ] No API keys in commit history (using placeholders)

### **2. Vercel Account**
- [ ] Vercel account created at [vercel.com](https://vercel.com)
- [ ] Connected to GitHub account
- [ ] Access to `GoliathBritton` organization

### **3. Environment Variables**
- [ ] `VITE_SUPABASE_URL` = `https://hysfiibfajydjatsqtbz.supabase.co`
- [ ] `VITE_SUPABASE_ANON_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5c2ZpaWJmYWp5ZGphdHNxdGJ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0NjQzNjMsImV4cCI6MjA3MDA0MDM2M30.7bwhYLgCkHSlQXc14NuCpOY6y4jd8MjMc8zOIqynGjE`
- [ ] `VITE_WEBSITE_URL` = `https://flyfoxai.com`
- [ ] `VITE_APP_URL` = `https://app.flyfoxai.com`
- [ ] `VITE_API_URL` = `https://api.flyfoxai.com`
- [ ] `VITE_VOICE_URL` = `https://voice.flyfoxai.com`
- [ ] `VITE_STRIPE_PUBLISHABLE_KEY` = `pk_test_placeholder_key_here`
- [ ] `VITE_PAYPAL_CLIENT_ID` = `ARbHoAvcE25ruW5AoK414FTnkW_ufJWWiPwPgHyyU7ypOyDLIRKvNpoaEOGyV4j8U6Wxvtk-3OjA-LxK`

### **4. Domain Configuration**
- [ ] DNS records updated (see `FLYFOX_AI_DNS_CONFIGURATION_GUIDE.md`)
- [ ] Custom domain added in Vercel: `app.flyfoxai.com`
- [ ] SSL certificate provisioned

## **Deployment Steps**

### **Step 1: Import Project**
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import: `GoliathBritton/flyfox-ai-platform`
4. Vercel will auto-detect **Vite** framework

### **Step 2: Configure Settings**
1. **Framework Preset**: `vite` (auto-detected)
2. **Root Directory**: `flyfox-ai-platform`
3. **Build Command**: `npm run build`
4. **Output Directory**: `dist`
5. **Install Command**: `npm install`

### **Step 3: Add Environment Variables**
1. Go to Project Settings → Environment Variables
2. Add all `VITE_*` variables listed above
3. Set to "Production" environment

### **Step 4: Add Custom Domain**
1. Go to Project Settings → Domains
2. Add: `app.flyfoxai.com`
3. Follow DNS configuration guide

### **Step 5: Deploy**
1. Click "Deploy"
2. Monitor build process
3. Verify deployment success

## **Post-Deployment Verification**

### **Build Success**
- [ ] Build completes without errors
- [ ] TypeScript compilation passes
- [ ] All dependencies installed
- [ ] Output files generated in `dist/`

### **Domain Access**
- [ ] `https://app.flyfoxai.com` loads correctly
- [ ] SSL certificate is active
- [ ] No mixed content warnings

### **Functionality Test**
- [ ] React app loads
- [ ] Supabase connection works
- [ ] Payment buttons render
- [ ] Navigation works
- [ ] Responsive design works

### **Performance Check**
- [ ] Page load time < 3 seconds
- [ ] No console errors
- [ ] Images load correctly
- [ ] CSS/JS files load

## **Expected URLs After Deployment**

- **Production**: `https://app.flyfoxai.com`
- **Preview**: `https://flyfox-ai-platform-git-main-goliathbritton.vercel.app`
- **API**: `https://api.flyfoxai.com` (separate deployment)
- **Voice**: `https://voice.flyfoxai.com` (separate deployment)

## **Troubleshooting**

### **Build Failures**
- Check `package.json` for all dependencies
- Verify TypeScript compilation locally
- Check Vercel build logs for specific errors

### **Domain Issues**
- Verify DNS records are correct
- Allow 24-48 hours for propagation
- Check SSL certificate status

### **Environment Variables**
- Ensure all `VITE_*` variables are set
- Redeploy after adding new variables
- Check variable names match code

## **Success Criteria**

✅ **Framework**: Vite + React properly configured  
✅ **Build**: Successful compilation and deployment  
✅ **Domain**: Custom domain working with SSL  
✅ **Environment**: All variables properly set  
✅ **Performance**: Fast loading and responsive design  

---

**Status**: Ready for Vercel deployment with Vite framework preset!
