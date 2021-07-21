import os
path = '/home/shawn/Projects/Dataset/ardupilot/record_711/frames'
files = os.listdir(path)

number_files = len(files)

count = 0
for i in range(number_files):
    if os.path.isfile(os.path.join(path,'frame_'+str(i)+'.jpg')):
        os.rename(os.path.join(path,'frame_'+str(i)+'.jpg'), os.path.join(path,'frame_'+str(count)+'.jpg'))
        count += 1
    else:
        print("frame_{}.jpg does not exist.\n".format(i))

    