# 🚀 FLYFOX AI - DNS CONFIGURATION GUIDE
## **Complete DNS Setup for flyfoxai.com**

### **📋 CURRENT DNS RECORDS (DO NOT DELETE)**

Your domain currently has these records that should be **KEPT**:

```
A Record: flyfoxai.com → 44.223.112.86 (AWS Server)
CNAME: www → cname.deal.ai
CNAME: api → brand.ludicrous.cloud
CNAME: app → whitelabel.deal.ai
CNAME: voice → cname.deal.ai
CNAME: agents → brand.ludicrous.cloud
MX Records: Configured for emailsrvr.com
TXT Records: SPF, DKIM configured
```

### **🔧 REQUIRED DNS CHANGES**

#### **Step 1: Update Subdomain CNAME Records**

You need to update these CNAME records to point to Vercel:

**Current → New Configuration:**

```
CNAME: app → whitelabel.deal.ai → cname.vercel-dns.com
CNAME: api → brand.ludicrous.cloud → cname.vercel-dns.com  
CNAME: voice → cname.deal.ai → cname.vercel-dns.com
```

#### **Step 2: Keep These Records Unchanged**

```
A Record: flyfoxai.com → 44.223.112.86 (KEEP)
CNAME: www → cname.deal.ai (KEEP)
CNAME: agents → brand.ludicrous.cloud (KEEP)
MX Records: emailsrvr.com (KEEP)
TXT Records: SPF, DKIM (KEEP)
```

### **🚀 FINAL DNS CONFIGURATION**

After updates, your DNS should look like this:

```
# Main Domain
A Record: flyfoxai.com → 44.223.112.86

# Subdomains for FLYFOX AI Platform
CNAME: www → cname.deal.ai
CNAME: app → cname.vercel-dns.com
CNAME: api → cname.vercel-dns.com
CNAME: voice → cname.vercel-dns.com
CNAME: agents → brand.ludicrous.cloud

# Email Configuration
MX: flyfoxai.com → mx1.emailsrvr.com
MX: flyfoxai.com → mx2.emailsrvr.com

# Security Records
TXT: flyfoxai.com → "v=spf1 include:emailsrvr.com ~all"
TXT: k1._domainkey.lc → "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDbbcmAKfqiAADEdZkwjYCsiOmNUC1f3dwIrhVfVf13dHk33ba6hFaG0kYebOaOdLxG+bw2tL8+h00P6Wgr2Aq9G29kY1q+tu8MpsqZRA26oQSz7fqQul4wdNJtrAxxvqZ1ORgKOBatobVmQ9atf+k0YtNwG3BcF9oqtv7HBAdEzQIDAQAB"
TXT: lc → "v=spf1 include:mailgun.org ~all"
```

### **📱 STEP-BY-STEP DNS UPDATE INSTRUCTIONS**

#### **Option 1: Your Domain Provider Dashboard**

1. **Login to your domain provider** (where you purchased flyfoxai.com)
2. **Navigate to DNS Management**
3. **Find the CNAME records for:**
   - `app.flyfoxai.com`
   - `api.flyfoxai.com` 
   - `voice.flyfoxai.com`
4. **Update the values to:** `cname.vercel-dns.com`
5. **Save changes**

#### **Option 2: Command Line (if you have DNS API access)**

```bash
# Example using a DNS provider API
# Replace with your actual DNS provider commands

# Update app subdomain
dns update cname app.flyfoxai.com cname.vercel-dns.com

# Update api subdomain  
dns update cname api.flyfoxai.com cname.vercel-dns.com

# Update voice subdomain
dns update cname voice.flyfoxai.com cname.vercel-dns.com
```

### **🔍 DNS VERIFICATION**

After making changes, verify with these commands:

```bash
# Check DNS propagation
nslookup app.flyfoxai.com
nslookup api.flyfoxai.com
nslookup voice.flyfoxai.com

# Expected results should point to Vercel
```

### **⏱️ DNS PROPAGATION TIMELINE**

- **Immediate**: Some DNS providers update instantly
- **5-15 minutes**: Most providers propagate within this timeframe
- **24-48 hours**: Full global propagation (rare cases)
- **Recommended wait time**: 30 minutes before testing

### **🚀 DEPLOYMENT ARCHITECTURE**

After DNS updates, your platform will be accessible at:

```
🌐 Main Website: https://flyfoxai.com
📱 Frontend App: https://app.flyfoxai.com
🔧 API Services: https://api.flyfoxai.com
🎤 Voice Services: https://voice.flyfoxai.com
🤖 Agent Services: https://agents.flyfoxai.com
```

### **🔐 SSL CERTIFICATE STATUS**

- **Vercel Domains**: Automatic SSL certificates
- **AWS Lambda**: SSL handled by API Gateway
- **Supabase**: SSL included in service
- **Status**: All domains will have HTTPS automatically

### **📊 MONITORING DNS CHANGES**

#### **Vercel Dashboard**
```
URL: https://vercel.com/dashboard
Domains: app.flyfoxai.com, api.flyfoxai.com, voice.flyfoxai.com
Status: Will show "Pending" until DNS propagates
```

#### **DNS Health Check**
```bash
# Test domain resolution
curl -I https://app.flyfoxai.com
curl -I https://api.flyfoxai.com
curl -I https://voice.flyfoxai.com
```

### **⚠️ IMPORTANT NOTES**

1. **Don't delete existing records** - Only update the CNAME values
2. **Keep MX records** - Email functionality depends on these
3. **Keep TXT records** - Email security (SPF, DKIM) depends on these
4. **Wait for propagation** - DNS changes can take up to 48 hours globally
5. **Test gradually** - Start with one subdomain, then add others

### **🎯 SUCCESS CRITERIA**

Your DNS configuration is successful when:

- ✅ `app.flyfoxai.com` resolves to Vercel
- ✅ `api.flyfoxai.com` resolves to Vercel  
- ✅ `voice.flyfoxai.com` resolves to Vercel
- ✅ `flyfoxai.com` still points to your AWS server
- ✅ Email continues to work normally
- ✅ All SSL certificates are valid

### **📞 SUPPORT**

If you encounter issues:

1. **Check DNS propagation**: Use online DNS checkers
2. **Verify Vercel domains**: Check Vercel dashboard
3. **Contact support**: Your domain provider or Vercel support
4. **Emergency rollback**: Revert CNAME changes if needed

---

## **🚀 READY FOR DEPLOYMENT**

Once DNS is configured, your FLYFOX AI platform will be accessible at:
- **Frontend**: https://app.flyfoxai.com
- **API**: https://api.flyfoxai.com  
- **Voice**: https://voice.flyfoxai.com
- **Main**: https://flyfoxai.com

**Next Step**: Deploy your React app to Vercel and configure the custom domains!
