import os, fileinput

def comments(file):
    filename, file_extension = os.path.splitext(file)
    print(file_extension)
    if file_extension in ['.js', '.cls', '.trigger']:
        return '// TO RESOLVE CONFLICTS\n'
    elif file_extension in ['']:
        return '# TO RESOLVE CONFLICTS\n'
    else:
        return ''

paths = ['../force-app/main/default/staticresources', '../force-app/main/default/classes', '../force-app/main/default/aura', '../force-app/main/default/triggers']
listFailed = []

action = input('insert or remove comments? [i/r]: ')

for path in paths:
    listFile = os.listdir(path)
    size = len(listFile)
    print('--')
    print(path)
    for i, filename in enumerate(listFile):
        try:
            file = open(path + '/' +filename, 'r+')
            comment = comments(path + '/' +filename)
            print(comment)
            data = file.readlines()

            for line, value in enumerate(data):
                if action == 'i':
                    data[line] = comment + value
                else:
                    data[line] = value.replace(comment, '')
            with open(path + '/' +filename, 'w') as file:
                file.writelines( data )
        except:
            listFailed.append(filename)
            print("Something went wrong")
        finally:
            print(str(i + 1) + " of " + str(size))
    print(path)
    print('--\n')


print("\nFinished")
print("Failed items: ")
print(listFailed)