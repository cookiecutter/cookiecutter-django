git rm -r --cached .
git add -A
echo "Enter comment"
read comment
git commit -am $comment
git push
