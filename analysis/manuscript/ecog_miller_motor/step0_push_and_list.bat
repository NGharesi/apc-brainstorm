@echo off
cd /d C:\Users\nghare\.brainstorm\process\revision_checks\ecog_miller_motor
echo step0 start %date% %time% > step0.log
git -C C:\Users\nghare\.brainstorm\process\apc-brainstorm-publish push origin neuroimage-submission >> step0.log 2>&1
echo push_exit %errorlevel% >> step0.log
git -C C:\Users\nghare\.brainstorm\process\apc-brainstorm-publish ls-remote origin refs/heads/neuroimage-submission >> step0.log 2>&1
curl.exe -sSL -o purl_page.html https://purl.stanford.edu/zk881ps0522 >> step0.log 2>&1
echo curl_exit %errorlevel% >> step0.log
where matlab >> step0.log 2>&1
echo step0 done >> step0.log
