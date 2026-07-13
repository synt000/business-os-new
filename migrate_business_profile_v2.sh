sqlite3 business.db <<'SQL'

ALTER TABLE business_profiles ADD COLUMN business_slug TEXT;
ALTER TABLE business_profiles ADD COLUMN welcome_message TEXT;
ALTER TABLE business_profiles ADD COLUMN cover_url TEXT;
ALTER TABLE business_profiles ADD COLUMN email TEXT;
ALTER TABLE business_profiles ADD COLUMN website_url TEXT;
ALTER TABLE business_profiles ADD COLUMN owner_name TEXT;
ALTER TABLE business_profiles ADD COLUMN owner_phone TEXT;
ALTER TABLE business_profiles ADD COLUMN facebook_username TEXT;
ALTER TABLE business_profiles ADD COLUMN telegram_username TEXT;
ALTER TABLE business_profiles ADD COLUMN viber_number TEXT;
ALTER TABLE business_profiles ADD COLUMN facebook_url TEXT;
ALTER TABLE business_profiles ADD COLUMN telegram_url TEXT;
ALTER TABLE business_profiles ADD COLUMN qr_code TEXT;

UPDATE business_profiles
SET business_slug = lower(replace(business_name,' ','-'))
WHERE business_slug IS NULL;

SQL

echo "✅ Business Profile Migration Complete"

sqlite3 business.db "PRAGMA table_info(business_profiles);"

