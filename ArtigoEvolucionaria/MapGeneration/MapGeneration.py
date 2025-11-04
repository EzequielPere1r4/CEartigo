import queue
import random
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from Models.Chromosome import Chromosome # Importa para a visualização
from Models.Gene import Gene # Importa para a visualização

class Corridor:
    # ... (código idêntico ao da sua versão anterior) ...
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def createCorridor(self, start, end):
        corridor = []
        position = start.copy()
        corridor.append(position.copy())
        while abs(position[1] - end[1]) > 0.01:
            if position[1] < end[1]:
                position[1] += 1.0
                if position[1] > end[1]: position[1] = end[1]
            else:
                position[1] -= 1.0
                if position[1] < end[1]: position[1] = end[1]
            corridor.append(position.copy())
            if abs(position[1] - end[1]) < 0.01:
                position[1] = end[1]
                break
        while abs(position[0] - end[0]) > 0.01:
            if position[0] < end[0]:
                position[0] += 1.0
                if position[0] > end[0]: position[0] = end[0]
            else:
                position[0] -= 1.0
                if position[0] < end[0]: position[0] = end[0]
            corridor.append(position.copy())
            if abs(position[0] - end[0]) < 0.01:
                position[0] = end[0]
                break
        final_pos = [end[0], end[1]]
        if abs(corridor[-1][0] - final_pos[0]) > 0.01 or abs(corridor[-1][1] - final_pos[1]) > 0.01:
            corridor.append(final_pos)
        return corridor
    def __str__(self): return f"Corridor(start=({self.start[0]}, {self.start[1]}), end=({self.end[0]}, {self.end[1]}))"
    def __repr__(self): return self.__str__()

class Room:
    # ... (código idêntico ao da sua versão anterior) ...
    def __init__(self, x, y, width, height):
        self.number = None; self.center = None; self.width = width; self.height = height
        self.xStart = x; self.yStart = y; self.xEnd = x + width; self.yEnd = y + height
    def splitHorizontal(self, room, dividePoint, roomQueue ):
        roomQueue.put(Room(room.xStart, room.yStart, dividePoint, room.height))
        roomQueue.put(Room(room.xStart + dividePoint, room.yStart, room.width - dividePoint, room.height))
    def splitVertical(self, room, dividePoint, roomQueue ):
        roomQueue.put(Room(room.xStart, room.yStart, room.width, dividePoint))
        roomQueue.put(Room(room.xStart, room.yStart + dividePoint, room.width, room.height - dividePoint))
    def __str__(self):
        number_str = f"#{self.number}" if self.number is not None else ""
        return f"Room{number_str}(pos=({self.xStart}, {self.yStart}), size=({self.width}x{self.height}), end=({self.xEnd}, {self.yEnd}))"
    def __repr__(self): return self.__str__()

class Map:
    # ... (código idêntico ao da sua versão anterior, MAS com visualize_map ATUALIZADO) ...
    def __init__(self, mapWidth, mapHeight, minRoomWidth, minRoomHeight, offset=1):
        self.mapWidth = mapWidth; self.mapHeight = mapHeight; self.minRoomWidth = minRoomWidth
        self.minRoomHeight = minRoomHeight; self.offset = offset

    def generate_map(self):
        roomQueue = queue.Queue(); roomList = []; roomQueue.put(Room(0, 0, self.mapWidth, self.mapHeight))
        while not roomQueue.empty():
            room = roomQueue.get()
            if random.random() < 0.5:
                if room.width >= self.minRoomWidth * 2:
                    dividePoint = random.randint(self.minRoomWidth, room.width - self.minRoomWidth)
                    room.splitHorizontal(room, dividePoint, roomQueue)
                elif room.height >= self.minRoomHeight * 2:
                    dividePoint = random.randint(self.minRoomHeight, room.height - self.minRoomHeight)
                    room.splitVertical(room, dividePoint, roomQueue)
                else: roomList.append(room)
            else:
                if room.width >= self.minRoomWidth * 2:
                    dividePoint = random.randint(self.minRoomWidth, room.width - self.minRoomWidth)
                    room.splitHorizontal(room, dividePoint, roomQueue)
                elif room.height >= self.minRoomHeight * 2:
                    dividePoint = random.randint(self.minRoomHeight, room.height - self.minRoomHeight)
                    room.splitVertical(room, dividePoint, roomQueue)
                else: roomList.append(room)
        roomCenterList = []
        for i, room in enumerate(roomList):
            room.number = i + 1; room.center = [room.xStart + room.width / 2, room.yStart + room.height / 2]
            roomCenterList.append(room.center)
        self.applyOffset(roomList); corridorList = self.connectRooms(roomCenterList); return roomList, corridorList
    def calculateCorridorWidth(self): minDimension = min(self.mapWidth, self.mapHeight); return max(1.0, minDimension * 0.05)
    def isPointInsideRoom(self, point, room): return (room.xStart <= point[0] <= room.xEnd and room.yStart <= point[1] <= room.yEnd)
    def isRectangleInsideRoom(self, rect_x, rect_y, rect_width, rect_height, room):
        corners = [[rect_x, rect_y], [rect_x + rect_width, rect_y], [rect_x, rect_y + rect_height], [rect_x + rect_width, rect_height]]
        return all(self.isPointInsideRoom(corner, room) for corner in corners)
    def createCorridorRectangles(self, corridor_path, width, rooms):
        rectangles = []; half_width = width / 2.0
        for i in range(len(corridor_path) - 1):
            p1 = corridor_path[i]; p2 = corridor_path[i + 1]; dx = p2[0] - p1[0]; dy = p2[1] - p1[1]
            if abs(dy) < 0.01:
                x = min(p1[0], p2[0]); y = p1[1] - half_width; rect_width = abs(dx) if abs(dx) > 0.01 else 1.0; rect_height = width
            elif abs(dx) < 0.01:
                x = p1[0] - half_width; y = min(p1[1], p2[1]); rect_width = width; rect_height = abs(dy) if abs(dy) > 0.01 else 1.0
            else:
                x = min(p1[0], p2[0]) - half_width; y = min(p1[1], p2[1]) - half_width; rect_width = abs(dx) + width; rect_height = abs(dy) + width
            is_inside_room = any(self.isRectangleInsideRoom(x, y, rect_width, rect_height, room) for room in rooms)
            if not is_inside_room: rectangles.append({'x': x, 'y': y, 'width': rect_width, 'height': rect_height})
        return rectangles
    def connectRooms(self, roomCenterList):
        corridorList = []; currentRoomCenter = random.choice(roomCenterList); roomCenterList.remove(currentRoomCenter)
        while len(roomCenterList) > 0:
            closestRoomCenter = self.findClosestRoomCenter(currentRoomCenter, roomCenterList); roomCenterList.remove(closestRoomCenter)
            corridor = Corridor(currentRoomCenter, closestRoomCenter); corridorList.append(corridor.createCorridor(currentRoomCenter, closestRoomCenter))
            currentRoomCenter = closestRoomCenter
        return corridorList
    def findClosestRoomCenter(self, currentRoomCenter, roomCenterList):
        closestRoomCenter = None; closestDistance = float('inf')
        for roomCenter in roomCenterList:
            distance = self.calculateDistance(currentRoomCenter, roomCenter)
            if distance < closestDistance: closestDistance = distance; closestRoomCenter = roomCenter
        return closestRoomCenter
    def calculateDistance(self, currentRoomCenter, roomCenter): return math.sqrt((currentRoomCenter[0] - roomCenter[0]) ** 2 + (currentRoomCenter[1] - roomCenter[1]) ** 2)
    def applyOffset(self, roomList):
        for room in roomList:
            room.xStart += self.offset; room.xEnd -= self.offset; room.width = room.xEnd - room.xStart
            room.yStart += self.offset; room.yEnd -= self.offset; room.height = room.yEnd - room.yStart

    def visualize_map(self, rooms, corridors, chromosome: Chromosome = None):
        """ ATUALIZADO: Agora pode receber um cromossomo para plotar os inimigos """
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        common_color = '#4A90E2'
        
        for i, room in enumerate(rooms):
            rect = patches.Rectangle(
                (room.xStart, room.yStart), room.width, room.height,
                linewidth=2, edgecolor='black', facecolor=common_color, alpha=0.7
            )
            ax.add_patch(rect)
            
            center_x = room.xStart + room.width / 2
            center_y = room.yStart + room.height / 2
            
            # Se um cromossomo foi passado, exibe as infos do gene
            if chromosome:
                gene = chromosome.genes[i]
                gene_text = f"Sala {i+1}\n"
                gene_text += f"{''.join(gene.enemy_letters)}\n"
                gene_text += f"Dific.: {gene.difficulty}"
                if gene.bear_count > 0:
                    gene_text += "\n(CHEFE)"
                ax.text(center_x, center_y, gene_text, ha='center', va='center', fontsize=8, fontweight='bold', color='black')
            else:
                ax.text(center_x, center_y, str(i + 1), ha='center', va='center', fontsize=8, fontweight='bold')
        
        corridorWidth = self.calculateCorridorWidth()
        
        for i, corridor_path in enumerate(corridors):
            if len(corridor_path) > 1:
                rectangles = self.createCorridorRectangles(corridor_path, corridorWidth, rooms)
                for rect_data in rectangles:
                    rect = patches.Rectangle(
                        (rect_data['x'], rect_data['y']), rect_data['width'], rect_data['height'],
                        linewidth=0, edgecolor='none', facecolor=common_color, alpha=0.6
                    )
                    ax.add_patch(rect)
        
        ax.set_xlim(0, self.mapWidth)
        ax.set_ylim(0, self.mapHeight)
        ax.set_aspect('equal')
        ax.set_xlabel('Largura', fontsize=12)
        ax.set_ylabel('Altura', fontsize=12)
        
        if chromosome:
            ax.set_title(f'Mapa Gerado - Fitness: {chromosome.fitness:.2f}', fontsize=14, fontweight='bold')
        else:
            ax.set_title(f'Mapa Gerado - {len(rooms)} Salas', fontsize=14, fontweight='bold')
            
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.invert_yaxis()
        plt.tight_layout()
        # plt.show() # Removido 'show()' para ser chamado pelo main.py
        return fig, ax