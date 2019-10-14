ksql http://localhost:8088 <<EOF
RUN SCRIPT './ksql/scripts/views_page.sql';
RUN SCRIPT './ksql/scripts/impressions_ad.sql';
exit
EOFs