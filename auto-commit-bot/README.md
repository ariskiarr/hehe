# Auto-commit & push bot

Repo: d:/BOT/auto-commit-bot

Ringkasan (Indonesia):

- Script ini membuat/menyentuh file kecil di dalam repo lokal Anda, lalu menjalankan `git add`, `git commit`, dan `git push`.
- Tujuan: membuat commit harian/terjadwal sehingga GitHub menunjukkan aktivitas (contribution) di timeline Anda.

Penting - bacalah sebelum menjalankan:

- Pastikan Anda paham kebijakan GitHub terkait manipulasi kontribusi. Mengotak-atik grafik kontribusi untuk menipu orang lain tidak direkomendasikan.
- GitHub hanya menghitung kontribusi jika email commit cocok dengan email akun GitHub Anda, dan commit terjadi di branch default (biasanya `main`/`master`) atau pada repo yang dihitung untuk contributions.
- Otentikasi: gunakan SSH key atau credential helper agar `git push` tidak meminta sandi interaktif.

File utama:

- `commit_bot.py` — Python script yang melakukan touch file, commit, dan push.
- `create_task.ps1` — PowerShell helper untuk membuat Scheduled Task Windows agar script berjalan setiap hari.

Langkah cepat (contoh):

1. Salin/move script ke folder yang dapat diakses. Atau jalankan langsung dari path `d:/BOT/auto-commit-bot`.

2. Siapkan repo target (contoh: C:\path\to\my-repo). Pastikan repo sudah di-clone di mesin ini.

3. Pastikan git user yang dipakai cocok dengan akun GitHub Anda:

   Open PowerShell and run:

   git -C "C:/path/to/my-repo" config user.name "Your Name"
   git -C "C:/path/to/my-repo" config user.email "you@example.com"

4. Test run sekali manually (PowerShell):

   python "d:/BOT/auto-commit-bot/commit_bot.py" --repo "C:/path/to/my-repo" --branch main

   - If it prints "Committed and pushed successfully.", you're good. Check GitHub for the commit.

5. Create a scheduled task to run daily at 09:00 (example):

   powershell -ExecutionPolicy Bypass -File "d:/BOT/auto-commit-bot/create_task.ps1" -ScriptPath "d:/BOT/auto-commit-bot/commit_bot.py" -Time "09:00"

Notes & troubleshooting:

- If push fails with auth errors, ensure:
  - You have an SSH key added to your GitHub account and the repo uses SSH remote (git@github.com:...)
  - Or configure a credential helper that stores an access token (PAT) and use HTTPS remote.
- If GitHub doesn't count the commit as yours, check `git log -1 --pretty=full` to see author/committer email.

Safety & ethics:

- This tool automates commits. Don't use it to falsify work records, deceive others, or violate platform terms.

Next steps (optional):

- Add more intelligent change generation instead of simple append (e.g., update a harmless JSON with counts).
- Add logging to a file and rotation.

-- End
