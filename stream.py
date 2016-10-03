import sys
import io

import streaming

if __name__ == '__main__':
   keywords = sys.argv[1:]
   output_path = "data/" + "_".join(keywords) + ".txt"
   with io.open(output_path, 'w') as output_file:
      streaming.stream(keywords,language='en',output_file=output_file,max_count=10000)

