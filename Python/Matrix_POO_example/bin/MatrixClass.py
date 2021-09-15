#   Data Architect Academy
# Student : Maximiliano Nicolas Barrios
# Python Excercises
import copy
import logging


class Matrix:
        def __init__(self, incoming_rows):
            '''
            :param incoming_rows: Constructor of the class, receives a list
            of list that contains the rows of the matrix.
            '''
            logging.basicConfig(format='%(asctime)s %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p')
            if len(incoming_rows)>0:
                self.count_cols = len(incoming_rows[0])
                self.count_rows = len(incoming_rows)
            else :
                self.count_cols=0
                self.count_rows=0
            self.rows = incoming_rows
            self.columns = [ [row[index] for row in incoming_rows]
                             for index in range(self.count_cols)]

        def __repr__(self):
            ''':return: string in Matrix representation of the class'''
            rows_parsed = str(self.rows)
            rows_parsed = rows_parsed.replace("]," , "],\n\t\t\t  ")
            return "Matrix : " + rows_parsed

        def __add__(self, other):
            '''
            :param other: Matrix
            :return: addition of original Matrix and other Matrix
            '''
            if isinstance(other, Matrix):
                if self.count_cols == other.count_cols and self.count_rows == other.count_rows:
                    return Matrix([ [ self.rows[index_row][index_col] + other.rows[index_row][index_col]
                                            for index_col in range(self.count_cols)]
                                            for index_row in range(self.count_rows) ])
                else:
                    logging.error("Matrix - add method : Wrong matrix dimensions.")
                    return None
            else:
                logging.error("Matrix - add method : Wrong type param input.")
                return None

        def __mul__(self, other):
            '''
            :param other: can be an scalar or Matrix
            :return: scalar multiplication result or Matrix multiplication result
            '''
            if isinstance(other, int) == True or isinstance(other, float) ==True:
                return Matrix([[self.rows[index_row][index_col] * other
                                        for index_col in range(self.count_cols)]
                                        for index_row in range(self.count_rows)])
            if isinstance(other, Matrix) == True:
                if self.count_cols == other.count_rows:
                    return Matrix ( [[ self.mul_row_col( row= self_row ,column= other_column)
                                                for other_column in other.columns]
                                                for self_row in self.rows])

        def mul_row_col(self, row, column):
            '''
            :param row: row to multiply
            :param column: column to multiply
            :return: product of row by column (scalar)
            '''
            if len(row) == len(column):
                return sum( row[n] * column[n] for n in range(len(row)))
            else:
                logging.error("Matrix - mul_row_col method Error: wrong dimensions")

        def transpose(self):
            '''
            :return: transpose of Matrix
            '''
            if self.count_rows ==1 and self.count_cols ==1 :
                return self.rows[0]
            return Matrix([[self.rows[j][i] for j in range(self.count_rows)] for i in range(self.count_cols)])

        def determinant(self):  ##Metodo de cofactores
            '''
            :return: determinant of Matrix using cofactors method
            '''
            matriz = self.rows
            suma = 0
            if len(matriz) != len(matriz[0]):
                logging.error("Matrix - determinant method error: not nxn matrix.")
                return None
            #  Caso base, determinante de una matriz de 2x2
            if len(matriz) == 1:
                return matriz[0][0]
            if len(matriz) == 2 and len(matriz[0]) == 2:
                suma = matriz[0][0] * matriz[1][1] - matriz[1][0] * matriz[0][1]
                return suma
            else:
                for i in range(len(matriz)):  # Itero sobre las columnas
                    aux = copy.deepcopy(
                        matriz)  # Duplico la matriz para no modificar la original y poder hacer los cálculos bien
                    aux.remove(matriz[0])  # Elimino la primera fila
                    for j in range(len(aux)):  # Me muevo por las filas restantes
                        # Creo submatrices sin tener en cuenta la columna actual pero sí la fila
                        aux[j] = aux[j][0:i] + aux[j][i + 1:]
                        matrix_aux = Matrix(aux)
                    # Calculo los determinante de estas submatrices recursivamente y los sumo al total
                    suma += (-1) ** (i % 2) * matriz[0][i] * matrix_aux.determinant()
                return suma

        def get_minor(self, row, column):
            values = [
                [
                    self.rows[other_row][other_column]
                    for other_column in range(self.count_cols)
                    if other_column != column
                ]
                for other_row in range(self.count_rows)
                if other_row != row
            ]
            return Matrix(values).determinant()

        def get_cofactor(self, row, column):
            if (row + column) % 2 == 0:
                return self.get_minor(row, column)
            return -1 * self.get_minor(row, column)

        def minors(self):
            return Matrix(
                [
                    [self.get_minor(row, column) for column in range(self.count_cols)]
                    for row in range(self.count_rows)
                ]
            )

        def cofactors(self):
            return Matrix(
                [
                    [
                        self.minors().rows[row][column]
                        if (row + column) % 2 == 0
                        else self.minors().rows[row][column] * -1
                        for column in range(self.minors().count_cols)
                    ]
                    for row in range(self.minors().count_rows)
                ]
            )

        def adjugate(self):
            '''
            :return: adjugate of Matrix
            '''
            if self.count_cols != self.count_rows:
                logging.error("Matrix - adjugate method error: not nxn matrix.")
                return None
            values = [
                [self.cofactors().rows[column][row] for column in range(self.count_cols)]
                for row in range(self.count_rows)
            ]
            return Matrix(values)

        def inverse(self):
            '''
            :return: inverse of Matrix
            '''
            if self.count_cols != self.count_rows:
                logging.error("Matrix - inverse method error: not nxn matrix.")
                return None
            adj = self.adjugate()
            inv_det = 1/ self.determinant()
            return adj*inv_det

        def get_column(self, number_cols):
            '''
            :param number_cols: receives a list with number of columns to obtain
            :return: a Matrix object
            '''
            aux_cols = []
            for i in number_cols:
                if i <= self.count_cols:
                    if self.columns[i-1] not in aux_cols:
                        aux_cols.append(self.columns[i-1])
                else:
                    logging.error("Matrix - get_columns method: Index for column out of range")
            matrix_column = Matrix(aux_cols)
            matrix_column = matrix_column.transpose()
            return matrix_column

        def get_rows(self, number_rows):
            '''
            :param number_rows: receives a list with number of rows to obtain
            :return: Matrix object
            '''
            aux_rows = []
            for i in number_rows:
                if i <= self.count_rows:
                    if self.rows[i-1] not in aux_rows:
                        aux_rows.append(self.rows[i-1])
                else:
                    logging.error("Matrix - get_rows method: Index for row out of range")
            matrix_row = Matrix(aux_rows)
            return matrix_row

        def get_submatrix(self,
                                        dimension_row,
                                        dimension_col,
                                        index_row,
                                        index_col):
            aux_submatrix = []
            try:
                for i in range(dimension_row):
                    aux_submatrix.append([])
                    for j in range(dimension_col):
                        aux_submatrix[i].append(self.rows[index_row][index_col])
                        index_col+=1
                    index_row+=1
                    index_col = index_col - j -1
            except IndexError:
                logging.error("Matrix - get_submatrix method Error : Wrong index or params")
                return None
            return Matrix(aux_submatrix)


