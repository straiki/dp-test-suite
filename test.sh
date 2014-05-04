#!/usr/bin/sh

echo 'Test suite for DP -- vahalik tomas --'

if [ "$1" ] ; then
  DIRECTORY="$1"
else
  echo "test.sh <path_to_directory>"
  exit 1
fi

if [ -f ./$DIRECTORY/Reference ] ; then
 echo "Reference Exists"
else
  mkdir $DIRECTORY/Reference
fi
if [ -f ./$DIRECTORY/Current ] ; then
 echo "Current Exists"
else
  mkdir $DIRECTORY/Current
fi

echo "Copying files.."
cp `find $DIRECTORY/Original/ -name "*.jpg"`  $DIRECTORY/Reference/

echo "Creating reference model.."


#./CreateModel $DIRECTORY/Reference true > $DIRECTORY/Reference/output.txt


echo "Copying 5 random files"
mkdir $DIRECTORY/Current/Model
mkdir $DIRECTORY/Current/Localization
cp `find $DIRECTORY/Original/ -name "*.jpg"`  $DIRECTORY/Current/Model

files=`find $DIRECTORY/Current/Model/ -name "*.jpg" -type f | sort -R`
echo $files

counter=1
for file in ${files[@]} ; do 
  if [ [ $counter > 5 ] ] then ;
    break
  fi
  echo $file
  counter=$((counter+1))
done

#cp --backup=numbered "${files[@]}" $DIRECTORY/Current/Localization/


#./model_localization models/complex/Original/model_data.yaml models/complex/Original/12-9.jpg true

