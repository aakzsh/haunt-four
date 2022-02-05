

from random import randint


def winstatus(matrix, clr):
    for c in range(7-3):
        for r in range(7):
            if matrix[r][c] == clr and matrix[r][c+1] == clr and matrix[r][c+2] == clr and matrix[r][c+3]==clr:
                return True
    
    for c in range(7):
        for r in range(7-3):
            if matrix[r][c] == clr and matrix[r+1][c] == clr and matrix[r+2][c] == clr and matrix[r+3][c]==clr:
                return True

    for c in range(4):
        for r in range(7-3):
            if matrix[r][c] == clr and matrix[r+1][c+1] == clr and matrix[r+2][c+2] == clr and matrix[r+3][c+3]==clr:
                return True    

    for c in range(4):
        for r in range(3, 7):
            if matrix[r][c] == clr and matrix[r-1][c+1] == clr and matrix[r-2][c+2] == clr and matrix[r-3][c+3]==clr:
                return True        
    return False

    
        

def botstep(matrix, clr):
        a = randint(0,1)
        if a==1:
            for i in range(6,-1,-1):
                for x in range(len(matrix[i])):
                    if matrix[i][x]==2:
                        matrix[i][x]=clr
                        print("botbaamzi", matrix)
                        return matrix
        else:
            try:
                for i in range(6,-1,-1):
                    for x in range(len(matrix), -1,-1):
                        if matrix[x][i]==2:
                            matrix[i][x]=clr
                            print("botbaamzi", matrix)
                            return matrix
            except:
                for i in range(6,-1,-1):
                    for x in range(len(matrix[i])):
                        if matrix[i][x]==2:
                            matrix[i][x]=clr
                            print("botbaamzi", matrix)
                            return matrix


def winstatusbot(matrix, clr):
    return winstatus(matrix, clr)


