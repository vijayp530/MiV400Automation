import difflib
import time

# f1 = open(r'C:\test\authenticator-160127.000019-1.Log','rb')
# f2 = open(r'C:\test\authenticator-160127.000019-2.Log','rb')


def get_diff(old_file, new_file):
    f1 = open(old_file,'rb')
    f2 = open(new_file,'rb')

    old_file=f1.readlines()
    new_file=f2.readlines()

    diff = difflib.unified_diff(old_file, new_file, lineterm='')
    # for line in diff:
    #     print(line)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    return added
    # removed = [line[1:] for line in lines if line[0] == '-']
    # return removed


if __name__ == '__main__':
    f1 = r'C:\test\authenticator-160127.000019-1.Log'
    f2 = r'C:\test\authenticator-160127.000019-2.Log'
    with open('diff.log', 'wb') as f:
        f.write("".join(get_diff(f1,f2)))
