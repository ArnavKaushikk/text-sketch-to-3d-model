

from scripts.master_pipeline import run_pipeline
import sys
import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
import argparse
sys.path.append(os.path.abspath("app/TripoSR"))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input_type",type=str,required=True,choices=["text","sketch"],help="Type of input")
    parser.add_argument("--data",type=str,required=True,help="Text prompt or path to image")
    parser.add_argument("--multiview",action="store_true",help="Enable multiview generation")
    args=parser.parse_args()
    result=run_pipeline(input_type=args.input_type,data=args.data,use_multiview=args.multiview)
    print("Final STL at ",result)
if __name__=="__main__":
    main()