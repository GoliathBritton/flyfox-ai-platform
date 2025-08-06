# FLYFOX AI - DEPLOYMENT SUMMARY
## **Domain: flyfoxai.com**

### **Domain Structure**
- **Main Website**: https://flyfoxai.com
- **Application**: https://app.flyfoxai.com
- **API Services**: https://api.flyfoxai.com
- **Voice Services**: https://voice.flyfoxai.com

### **Deployment Components**

#### **Frontend (Vercel)**
```
Domain: https://app.flyfoxai.com
Project: flyfox-ai-platform/
Framework: React + TypeScript + Vite
Deployment: Vercel
```

#### **Backend (AWS Lambda)**
```
Domain: https://api.flyfoxai.com
Services: Python backend scripts
Hosting: AWS Lambda (44.223.112.86)
Database: Supabase (PostgreSQL)
```

#### **Voice Services (Vercel Functions)**
```
Domain: https://voice.flyfoxai.com
Services: Quantum voice calling
Hosting: Vercel Edge Functions
Integration: Nuco.Cloud quantum computing
```

### **DNS Configuration**
```
A Record: flyfoxai.com → 44.223.112.86 (AWS Server)
CNAME: www → cname.deal.ai
CNAME: app → cname.vercel-dns.com
CNAME: api → cname.vercel-dns.com
CNAME: voice → cname.vercel-dns.com
CNAME: agents → brand.ludicrous.cloud
```

### **Cost Structure**
- **Domain**: flyfoxai.com (already owned)
- **Vercel**: Free tier (100GB bandwidth)
- **Supabase**: Free tier (500MB database)
- **AWS Lambda**: Free tier (1M requests/month)
- **SSL**: Free (automatic)

### **Ready for Deployment**
All domain references have been updated to use flyfoxai.com!
