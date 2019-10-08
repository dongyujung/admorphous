ksql http://localhost:8088 <<EOF
RUN SCRIPT 'views_page.sql';
RUN SCRIPT 'impressions_ad.sql';
exit
EOFs