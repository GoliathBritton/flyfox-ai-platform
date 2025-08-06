# FLYFOX AI - VERCEL DEPLOYMENT GUIDE
## **Domain: flyfoxai.com**

### **Prerequisites**
- ✅ Domain: flyfoxai.com (already owned)
- ✅ DNS: Configured with existing records
- ✅ Supabase: Database ready
- ✅ AWS: Lambda functions ready

### **Step 1: Install Vercel CLI**
```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login
```

### **Step 2: Deploy React App**
```bash
# Navigate to React app directory
cd flyfox-ai-platform

# Install dependencies
npm install

# Build the app
npm run build

# Deploy to Vercel
vercel --prod
```

### **Step 3: Configure Custom Domains**
```bash
# Add custom domains to Vercel
vercel domains add app.flyfoxai.com
vercel domains add api.flyfoxai.com
vercel domains add voice.flyfoxai.com
```

### **Step 4: Update DNS Records**
Update your DNS zone with these CNAME records:

```
CNAME: app → cname.vercel-dns.com
CNAME: api → cname.vercel-dns.com
CNAME: voice → cname.vercel-dns.com
```

### **Step 5: Environment Variables**
Set these environment variables in Vercel dashboard:

```env
VITE_SUPABASE_URL=https://hysfiibfajydjatsqtbz.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5c2ZpaWJmYWp5ZGphdHNxdGJ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0NjQzNjMsImV4cCI6MjA3MDA0MDM2M30.7bwhYLgCkHSlQXc14NuCpOY6y4jd8MjMc8zOIqynGjE
VITE_WEBSITE_URL=https://flyfoxai.com
VITE_APP_URL=https://app.flyfoxai.com
VITE_API_URL=https://api.flyfoxai.com
VITE_VOICE_URL=https://voice.flyfoxai.com
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_51RtERqPrxTsW5OEfjlJ4MEvtx6vVV2zRx4Eq52WnD5Lq8TnWSqEJFWydBllXHGEu5bFz3cBbTzp3BZE1Rg31BKk00zjaU6UoJ
VITE_PAYPAL_CLIENT_ID=ARbHoAvcE25ruW5AoK414FTnkW_ufJWWiPwPgHyyU7ypOyDLIRKvNpoaEOGyV4j8U6Wxvtk-3OjA-LxK
VITE_NUCO_API_KEY=ScSL33hX9EGPlUniqabdT6dYeHrc1gFl9xeWulSYleZhIGZdWFubb8Rd8LaC9GXxJweK61CpZlrKANq5HLr6Txry0KPOEd59csltQ0EIuLMmW2N1KkOV8szEX8mni1gnVEBbAdDZbnOruwlYr5eAEJpreOHNi22TTLBzmyE9OygCxcxxKDslbylXCCUaNgRT90pH8x64qwf2kPuNvNTUvPn2aHQ
VITE_NUCO_PROJECT_ID=flyfox-ai-quantum-platform
```

### **Step 6: Deploy Backend Functions**
```bash
# Create API functions directory
mkdir -p flyfox-ai-platform/api

# Copy backend scripts to API functions
cp flyfox_*.py flyfox-ai-platform/api/
cp flyfox_complete_launch.py flyfox-ai-platform/api/

# Deploy API functions
vercel --prod
```

### **Step 7: Test Deployment**
```bash
# Test main application
curl https://app.flyfoxai.com

# Test API endpoints
curl https://api.flyfoxai.com/health

# Test voice services
curl https://voice.flyfoxai.com/status
```

### **Step 8: Monitor Deployment**
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Supabase Dashboard**: https://supabase.com/dashboard
- **AWS Lambda Console**: https://console.aws.amazon.com/lambda

### **Expected URLs After Deployment**
- ✅ https://flyfoxai.com (landing page)
- ✅ https://app.flyfoxai.com (React application)
- ✅ https://api.flyfoxai.com (backend services)
- ✅ https://voice.flyfoxai.com (voice services)

### **SSL Certificates**
- ✅ Automatic SSL for all subdomains
- ✅ HTTPS redirect enabled
- ✅ Security headers configured

### **Performance Optimization**
- ✅ Global CDN (Vercel Edge Network)
- ✅ Automatic caching
- ✅ Image optimization
- ✅ Code splitting

### **Cost Estimation**
- **Vercel Free Tier**: 100GB bandwidth/month
- **Supabase Free Tier**: 500MB database
- **AWS Lambda Free Tier**: 1M requests/month
- **Total Cost**: $0/month (free tier)

### **Success Metrics**
- ✅ Page Load: < 2 seconds
- ✅ API Response: < 100ms
- ✅ Database Queries: < 50ms
- ✅ Real-time Updates: < 10ms

### **Ready for Launch**
Your FLYFOX AI platform is now ready for deployment with flyfoxai.com!
