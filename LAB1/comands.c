python3 SearchIndex.py --index news --text good > text_good.txt
python3 SearchIndex.py --index news --query good AND evil > query_good_evil.txt
python3 SearchIndex.py --index news --text angle > text_angle.txt
python3 SearchIndex.py --index news --query angle~10> query_angle~10.txt
python3 CountWords.py --index news --alpha > news_alpha
