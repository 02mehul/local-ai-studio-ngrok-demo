const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log("Attempting to configure web/config.js from local Supabase status...");

exec('npx supabase status -o json', { cwd: path.join(__dirname, '..') }, (error, stdout, stderr) => {
    if (error) {
        console.error("Error running supabase status. Is Supabase running?");
        console.error(stderr);
        return;
    }

    try {
        const status = JSON.parse(stdout);
        const apiUrl = status.API_URL;
        const anonKey = status.ANON_KEY;

        if (!apiUrl || !anonKey) {
            console.error("Could not find API_URL or ANON_KEY in status output.");
            return;
        }

        const configPath = path.join(__dirname, '../web/config.js');
        let configContent = fs.readFileSync(configPath, 'utf8');

        // Replace URL
        configContent = configContent.replace(
            /SUPABASE_URL:.+,/,
            `SUPABASE_URL: '${apiUrl}',`
        );

        // Replace Key
        configContent = configContent.replace(
            /SUPABASE_KEY:.+,/,
            `SUPABASE_KEY: '${anonKey}',`
        );

        fs.writeFileSync(configPath, configContent);
        console.log("✅ Successfully updated web/config.js with local Supabase credentials!");
        console.log(`URL: ${apiUrl}`);
        console.log(`Key: ${anonKey.substring(0, 10)}...`);

    } catch (e) {
        console.error("Failed to parse status output:", e);
        console.log("Raw output:", stdout);
    }
});
