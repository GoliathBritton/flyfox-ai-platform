#!/usr/bin/env python3
"""
FLYFOX AI - Domain Reference Update Script
Updates all references from flyfoxai.com to flyfoxai.com
"""

import os
import re
import glob

def update_domain_references():
    """Update all domain references in the project"""
    print("🔄 Updating domain references from flyfoxai.com to flyfoxai.com...")
    
    # Files to update
    files_to_update = [
        "*.py",
        "*.md",
        "*.html",
        "*.ts",
        "*.tsx",
        "*.js",
        "*.json"
    ]
    
    updated_count = 0
    
    for pattern in files_to_update:
        for file_path in glob.glob(pattern, recursive=True):
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Update domain references
                    original_content = content
                    content = re.sub(r'flyfoxai\.io', 'flyfoxai.com', content)
                    content = re.sub(r'https://flyfoxai\.io', 'https://flyfoxai.com', content)
                    content = re.sub(r'https://app\.flyfoxai\.io', 'https://app.flyfoxai.com', content)
                    content = re.sub(r'https://api\.flyfoxai\.io', 'https://api.flyfoxai.com', content)
                    content = re.sub(r'https://voice\.flyfoxai\.io', 'https://voice.flyfoxai.com', content)
                    
                    # Update email addresses
                    content = re.sub(r'test@flyfoxai\.io', 'test@flyfoxai.com', content)
                    content = re.sub(r'demo@flyfoxai\.io', 'demo@flyfoxai.com', content)
                    content = re.sub(r'enterprise@flyfoxai\.io', 'enterprise@flyfoxai.com', content)
                    
                    # Only write if content changed
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated_count += 1
                        print(f"✅ Updated: {file_path}")
                        
                except Exception as e:
                    print(f"❌ Error updating {file_path}: {e}")
    
    print(f"\n🎉 Domain update complete! Updated {updated_count} files.")
    print("📋 Summary of changes:")
    print("   - flyfoxai.com → flyfoxai.com")
    print("   - app.flyfoxai.com → app.flyfoxai.com")
    print("   - api.flyfoxai.com → api.flyfoxai.com")
    print("   - voice.flyfoxai.com → voice.flyfoxai.com")
    print("   - Email addresses updated to @flyfoxai.com")

def create_deployment_summary():
    """Create a deployment summary with the new domain"""
    summary = """
# 🚀 FLYFOX AI - DEPLOYMENT SUMMARY
## **Domain: flyfoxai.com**

### **🌐 Domain Structure**
- **Main Website**: https://flyfoxai.com
- **Application**: https://app.flyfoxai.com
- **API Services**: https://api.flyfoxai.com
- **Voice Services**: https://voice.flyfoxai.com

### **📦 Deployment Components**

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

### **🔧 DNS Configuration**
```
A Record: flyfoxai.com → 44.223.112.86 (AWS Server)
CNAME: www → cname.deal.ai
CNAME: app → cname.vercel-dns.com
CNAME: api → cname.vercel-dns.com
CNAME: voice → cname.vercel-dns.com
CNAME: agents → brand.ludicrous.cloud
```

### **💰 Cost Structure**
- **Domain**: flyfoxai.com (already owned)
- **Vercel**: Free tier (100GB bandwidth)
- **Supabase**: Free tier (500MB database)
- **AWS Lambda**: Free tier (1M requests/month)
- **SSL**: Free (automatic)

### **🚀 Ready for Deployment**
All domain references have been updated to use flyfoxai.com!
"""
    
    with open("FLYFOX_AI_DEPLOYMENT_SUMMARY.md", "w") as f:
        f.write(summary)
    
    print("📄 Created: FLYFOX_AI_DEPLOYMENT_SUMMARY.md")

if __name__ == "__main__":
    update_domain_references()
    create_deployment_summary()
    print("\n🎉 FLYFOX AI platform is ready for deployment with flyfoxai.com!")
