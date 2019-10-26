keys=$(ls -1 ~/.screenlayout | sed -e 's/.sh//g' -e 's/_/ /g' -e '$ a Manual (arandr)')
values=$(ls -1 ~/.screenlayout | sed -e 's/^/~\/\.screenlayout\//' -e '$ a arandr')

result=$(echo "$keys" | dmenu -i -p "Layout Profile")
if [[ "$result" ]]; then
  matching_line_number=$(echo "$keys" | sed -n "/$result/ =")
  exec $(echo "$values" | sed -n "$matching_line_number p")
fi
