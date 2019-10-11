ksql http://localhost:8088 <<EOF
RUN SCRIPT '~/admorphous/ksql/scripts/views_page.sql';
RUN SCRIPT '~/admorphous/ksql/scripts/impressions_ad.sql';
exit
EOFs