ksql http://localhost:8088 <<EOF
RUN SCRIPT '~/admorphous/ksql/views_page.sql';
RUN SCRIPT '~/admorphous/ksql/impressions_ad.sql';
exit
EOFs