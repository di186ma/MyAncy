from django.shortcuts import render

from django.http import HttpResponseRedirect
from .forms import WayForm

from django.contrib import admin
from django.shortcuts import render
import cv2
from PIL import Image
import numpy as np
from .memory import SurSU
import time




def maze(request):
    startMaze = request.POST.get('start')
    finishMaze = request.POST.get('finish')
    class Point(object):

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def __add__(self, other):
            return Point(self.x + other.x, self.y + other.y)

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

    dir4 = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

    def BFS(s, e, h_maze, w_maze, img_maze, img_map):
        # const = 10000

        # cчетчик обработанных ячеек
        t = 0
        # длина пути
        l=0


        found = False
        q = []
        v = [[0 for j in range(w_maze)] for i in range(h_maze)]
        parent = [[Point() for j in range(w_maze)] for i in range(h_maze)]

        q.append(s)
        v[s.y][s.x] = 1
        while len(q) > 0:
            p = q.pop(0)
            for d in dir4:
                cell = p + d
                t+=1
                if (cell.x >= 0 and cell.x < w_maze and cell.y >= 0 and cell.y < h_maze and v[cell.y][cell.x] == 0 and
                        (img_maze[cell.y][cell.x][0] != 255 or img_maze[cell.y][cell.x][1] != 255 and img_maze[cell.y][cell.x][
                            2] != 255)):
                    q.append(cell)
                    v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later

                    # img[cell.y][cell.x] = list(reversed(
                    #     [i * 255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x] / const, 1, 1)])
                    # )
                    parent[cell.y][cell.x] = p
                    if cell == e:
                        found = True
                        del q[:]
                        break

        path = []
        if found:
            p = e
            while p != s:
                path.append(p)
                p = parent[p.y][p.x]
                l+=1
            path.append(p)
            path.reverse()

            rw = 2

            for p in path:
                cv2.rectangle(img_map, (p.x - rw, p.y - rw),
                              (p.x + rw, p.y + rw), (0, 100, 150), -1)

            print("Путь найден! Исследовано ячеек: ", t, "         Длина пути: ", l)
        else:
            print("Путь не найден!")

        return img_map

    def BBFS(s, e, h_maze, w_maze, img_maze, img_map):
        # const = 10000

        # cчетчик обработанных ячеек
        t = 0
        # длина пути
        l = 0

        found = False
        q = []
        v = [[0 for j in range(w_maze)] for i in range(h_maze)]
        parent = [[Point() for j in range(w_maze)] for i in range(h_maze)]

        q.append(s)
        v[s.y][s.x] = 1
        while len(q) > 0:
            p = q.pop(0)
            # p = q[-1]
            evr = abs(p.x - e.x) + abs(p.y - e.y)
            for d in dir4:
                cell = p + d
                t += 1

                if (cell.x >= 0 and cell.x < w_maze and cell.y >= 0 and cell.y < h_maze and v[cell.y][cell.x] == 0 and
                        (img_maze[cell.y][cell.x][0] != 255 or img_maze[cell.y][cell.x][1] != 255 and
                         img_maze[cell.y][cell.x][
                             2] != 255)):
                    if ((abs(cell.x - e.x) + abs(cell.y - e.y)) <= evr):
                        q.append(cell)
                        v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later

                        # img[cell.y][cell.x] = list(reversed(
                        #     [i * 255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x] / const, 1, 1)])
                        # )
                        parent[cell.y][cell.x] = p
                    else:
                        q.append(cell)
                        v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later

                        parent[cell.y][cell.x] = p

                    if cell == e:
                        q.append(cell)
                        parent[cell.y][cell.x] = p
                        print("Нашелся!")
                        found = True
                        del q[:]
                        # q.clear()
                        break

        path = []
        if found:
            p = e
            while p != s:
                path.append(p)
                p = parent[p.y][p.x]
                l += 1
            path.append(p)
            path.reverse()

            rw = 2

            for p in path:
                cv2.rectangle(img_map, (p.x - rw, p.y - rw),
                              (p.x + rw, p.y + rw), (0, 100, 150), -1)

            print("Путь найден! Исследовано ячеек: ", t, "         Длина пути: ", l)
        else:
            print("Путь не найден! Исследовано ячеек: ", t)

        return img_map


    pil_img_maze = Image.open(r'media/images/ready png/maze/'+startMaze[0]+'.png')
    img_maze = np.array(pil_img_maze)

    img_maze = cv2.cvtColor(img_maze, cv2.COLOR_BGR2RGB)
    img_maze = cv2.cvtColor(img_maze, cv2.COLOR_RGBA2GRAY)
    _, img_maze = cv2.threshold(img_maze, 15, 255, cv2.THRESH_BINARY)
    img_maze = cv2.cvtColor(img_maze, cv2.COLOR_GRAY2BGR)
    h_maze, w_maze = img_maze.shape[:2]

    img_map = np.asarray(Image.open(r'media/images/ready png/map/'+startMaze[0]+'.png').convert("RGB"))
    # img_map = Image.open(r'media/images/ready png/map/'+startMaze[0]+'.png').convert("RGB")

    if SurSU[startMaze[0] + " этаж"][startMaze]:
        sX=SurSU[startMaze[0] + " этаж"][startMaze][0]
        sY=SurSU[startMaze[0] + " этаж"][startMaze][1]

    if SurSU[finishMaze[0] + " этаж"][finishMaze]:
        eX=SurSU[finishMaze[0] + " этаж"][finishMaze][0]
        eY=SurSU[finishMaze[0] + " этаж"][finishMaze][1]

    # for kab in kabinets_7:
    #     if (startMaze == kab['num']):
    #         sX = kab['X']
    #         sY = kab['Y']
    #         break
    #
    # for kab in kabinets_7:
    #     if (finishMaze == kab['num']):
    #         eX = kab['X']
    #         eY = kab['Y']
    #         eX1 = kab_708['X']
    #         eY1 = kab_708['Y']
    #         break

    rw = 2

    cv2.rectangle(img_maze, (sX - rw, sY - rw),
                  (sX + rw, sY + rw), (0, 0, 255), -1)
    start = Point(sX, sY)
    print("start = ", start.x, start.y)

    cv2.rectangle(img_maze, (eX - rw, eY - rw),
                  (eX + rw, eY + rw), (0, 200, 50), -1)
    end = Point(eX, eY)
    print("end = ", end.x, end.y)

    # начало отсчета времени алгоритма
    startTime = time.time()
    img_map = BBFS(start, end, h_maze, w_maze, img_maze, img_map)
    endTime=time.time()

    print("Время работы алгоритма:", endTime-startTime, "секунд")

    # arr_map = np.array(img_map)
    img_map = np.asarray(img_map)
    img_map = Image.fromarray(img_map)
    print(type(img_map))

    img_map.save(r'media/images/ready png/result.png')

    return render(request, 'main/maze.html')


def main(request):
    if request.method == 'POST':
        form = WayForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = WayForm()

    return render(request, 'main/index.html', {'form': form})
