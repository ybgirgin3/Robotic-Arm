# run twice and open jpg files
# $1 : image url

# 3, 3 : yolov -> 3  weight -> 3
# 4, 4 : yolov -> 4  weight -> 4

# $1  : yolov/weight
# $3  : url


# for i in 3 4;
# do
#   echo "\n"
#   echo "looking for toothbrush"
#   echo "Processing:\n\t using yolo/weight: $i"
#   ./find_everything.py $i $1
#   echo "\n"
# done

# yolov4 sıkıntı çıkarabiliyor
# o yüzden 3'ü kullnıyoruz
./find_everything.py 3 $1
