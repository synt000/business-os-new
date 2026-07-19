# Business OS Master TODO Roadmap

📅 Current Phase:
Customer Onboarding + Business Identity Engine

---

## 🌍 MASTER VISION

Business OS က လုပ်ငန်းရှင်တွေကို Web တစ်ခုတည်းကနေ

✅ Facebook  
✅ TikTok  
✅ Telegram  
✅ Instagram  
✅ WhatsApp  

တို့နဲ့ ချိတ်ဆက်ပြီး လုပ်ငန်းအားလုံးကို စီမံနိုင်တဲ့
All-in-One Business Operating System ဖြစ်ရန်။

---

# ✅ COMPLETED

[x] SaaS Core Architecture

[x] Multi Tenant System

[x] Permission System

[x] Role Management

[x] Admin Permission UI

[x] Personal Permission Override

[x] Business Type Mapping System

[x] Feature Mapping Engine

[x] Tenant Feature Assignment Service

[x] JWT Authentication System

[x] JWT Token Claims Upgrade
    - user_id
    - tenant_id
    - role
    - business_type
    - subscription

[x] Login Token Generation Cleanup

[x] Register Schema Upgrade
    - business_type_code added


---

# 🚧 CURRENT WORK

[x] Customer Onboarding Engine

Goal:

Register လုပ်တဲ့အချိန်မှာ

Business Owner
        ↓
Select Business Type
        ↓
Create Tenant
        ↓
Attach Business Type
        ↓
Auto Assign Features
        ↓
Create Business Profile
        ↓
Generate Public Homepage


---

# NEXT STEPS

[x] Register API Business Type Integration

[x] Auto Feature Assignment During Signup

[ ] Auto BusinessProfile Creation  <-- CURRENT

[ ] Business Slug Generator

[ ] Public Business Homepage Upgrade

[ ] Landing Website Showcase

[ ] Business Rental System

[ ] Subscription System


---

# PROJECT RULE

အလုပ်တစ်ဆင့်ပြီးတိုင်း

[x] TODO.md update

[x] Git commit

[x] Test compile

[x] Record CHANGELOG



# ✅ Completed Checkpoints

## Sprint: Business Identity + SaaS Onboarding Core

### ✅ Business Type Onboarding
- [x] BusinessType Model integration
- [x] Business Type seed data created
- [x] Register payload supports business_type_code
- [x] Validate selected business type during registration
- [x] Tenant automatically linked with business_type_id

### ✅ Auto Feature Assignment
- [x] Feature assignment service connected
- [x] assign_features_to_tenant() integrated into owner registration flow
- [x] Business type based feature activation completed

### ✅ Business Profile Auto Creation
- [x] BusinessProfile auto create during owner registration
- [x] Tenant identity connected with BusinessProfile
- [x] Owner information stored
- [x] Public business profile foundation completed

### ✅ Business Slug System
- [x] Added slug generator service
- [x] File:
      src/domains/business_type/services/slug_service.py
- [x] Automatic public slug generation enabled

### ✅ Free Trial Subscription Foundation
- [x] SubscriptionPlan integration
- [x] FREE_TRIAL subscription creation
- [x] Trial activation during business registration

---

# 🚧 Next TODO

## Trial + Device Control System
- [ ] Create device module
- [ ] Device fingerprint storage
- [ ] 1 Device limit for FREE_TRIAL
- [ ] Device activation flow
- [ ] Device revoke management

## Giveaway / Promotion Engine
- [ ] Giveaway campaign model
- [ ] Promo code system
- [ ] Referral reward system
- [ ] Reward history tracking

