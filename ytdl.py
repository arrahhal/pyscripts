from pytube import YouTube


def text_bold(text):
    BOLD = '\033[1m'
    END = '\033[0m'
    return BOLD + text + END

def print_field(label, text):
    print(text_bold(label) + ": " + str(text))


print(text_bold("Youtube videos downloader"))

link = input("Enter the video link you want to download...\n")
yt = YouTube(link)

print_field('title', yt.title)
print_field('authur', yt.author)
print_field('views', yt.views)
print_field('length', str(yt.length // 60) + " m")
streams = yt.streams.filter(progressive=True).order_by('resolution').desc()

res_dict = {}
for stream in streams:
    res_dict[stream.resolution] = stream.itag

resolutions = []
for stream in streams:
    resolutions.append(stream.resolution)


input_mes = ''
for index, item in enumerate(resolutions):
    input_mes += f'{index+1}) {item}\n'
input_mes += 'Your Choice: '

user_input = ''
while user_input.lower() not in resolutions:
    user_input = input(input_mes)

chosen = streams.get_by_itag(res_dict[user_input])
if chosen is not None:
    print('donloading...')
    chosen.download()

