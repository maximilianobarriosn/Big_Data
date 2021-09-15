import logging
from unittest import TestCase
from fundamentals.Python_excercises.bin.MatrixClass import Matrix

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

class TestMatrix(TestCase):
    def test_add_matrix_successful(self):
        print("------ test_add_matrix_successful BEGIN : ------")
        tst_matrix_1 = Matrix([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])
        tst_matrix2 = Matrix([[1, 1, 1],
                               [1, 1, 1],
                               [1, 1, 1]])
        result_matrix = Matrix([[2,3,4],
                              [5,6,7],
                              [8,9,10]])
        matrix_under_tst = tst_matrix_1 + tst_matrix2
        self.assertEqual( matrix_under_tst.columns, result_matrix.columns)
        self.assertEqual(matrix_under_tst.rows, result_matrix.rows)
        print("Result = %s" %matrix_under_tst)
        print("------ test_add_matrix_successful END. ------\n")

    def test_add_matrix_wrong_dimensions(self):
        print("------ test_add_matrix_wrong_dimensions BEGIN : ------")
        tst_matrix_1 = Matrix([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])
        tst_matrix2 = Matrix([[1, 1, 1],
                               [1, 1, 1]])
        matrix_under_tst = tst_matrix_1 + tst_matrix2
        self.assertEqual( matrix_under_tst, None)
        print("Result = %s" %matrix_under_tst)
        print("------ test_add_matrix_wrong_dimensions END. ------\n")

    def test_add_matrix_wrong_input_scalar_and_matrix(self):
        print("------ test_add_matrix_wrong_input_scalar_and_matrix BEGIN : ------")
        tst_matrix_1 = Matrix([[1, 2, 3],
                             [4, 5, 6],
                             [7, 8, 9]])
        matrix_under_tst = tst_matrix_1 + 3
        self.assertEqual( matrix_under_tst, None)
        print("Result = %s" %matrix_under_tst)
        print("------ test_add_matrix_wrong_input_scalar_and_matrix END. ------\n")

    def test_mul_matrix_by_scalar(self):
        print("------ test_mul_matrix_by_scalar BEGIN : ------")
        tst_matrix = Matrix([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]])
        matrix_under_tst = tst_matrix*3
        result_matrix = Matrix([[3,3,3],
                              [3,3,3],
                              [3,3,3]])
        print("Original matrix : %s" %tst_matrix)
        print("Matrix * 3 = %s" %matrix_under_tst)
        print("------ test_mul_matrix_by_scalar END. ------\n")
        self.assertEqual(matrix_under_tst.columns, result_matrix.columns)
        self.assertEqual(matrix_under_tst.rows, result_matrix.rows)

    def test_mul_matrix_by_matrix(self):
        print("------ test_mul_matrix_by_matrix BEGIN : ------")
        result_matrix = Matrix([[7, 10],
                             [15, 22]])
        tst_matrix_1= Matrix([[1,2],
                            [3,4]])
        matrix_under_tst = tst_matrix_1 * tst_matrix_1
        print("Result = %s" %matrix_under_tst)
        print("------ test_mul_matrix_by_matrix END. ------\n")
        self.assertEqual( matrix_under_tst.columns, result_matrix.columns)
        self.assertEqual(matrix_under_tst.rows, result_matrix.rows)

    def test_mul_matrix_by_matrix_wrong_dimensions(self):
        print("------ test_mul_matrix_by_matrix_wrong_dimensions BEGIN : ------")
        tst_matrix_1= Matrix([[1,2],
                            [3,4]])
        tst_matrix_2 = Matrix([[1, 2, 4],
                               [3,5,6],
                               [3,5,6]])
        matrix_under_tst = tst_matrix_1 * tst_matrix_2
        print("Result = %s" %matrix_under_tst)
        print("------ test_mul_matrix_by_matrix_wrong_dimensions END. ------\n")
        self.assertEqual(matrix_under_tst, None)

    def test_matrix_transpose(self):
        print("------ test_matrix_transpose BEGIN : ------")
        tst_matrix = Matrix([[1, 2, 3,4],
                            [4, 5, 6,7],
                            [7, 8, 9,10]])
        result_matrix = Matrix([[1,4,7],
                              [2,5,8],
                              [3,6,9],
                              [4,7,10]])
        matrix_under_tst = tst_matrix.transpose()
        print("Original matrix: %s" %tst_matrix)
        print("Transpose matrix : %s " %result_matrix )
        print("------ test_matrix_transpose END. ------\n")
        self.assertEqual( matrix_under_tst.columns, result_matrix.columns)
        self.assertEqual(matrix_under_tst.rows, result_matrix.rows)

    def test_determinant(self):
        print("------ test_matrix_determinant BEGIN : ------")
        matrix_undertest = Matrix([[1, 51, 1], [2, 5, 31], [4, 4, 4]])
        det = matrix_undertest.determinant()
        print("Original matrix : %s " %matrix_undertest)
        print("Determinant = %s" %det)
        print("------ test_determinant END. ------\n")
        self.assertEqual(det, 5800)

    def test_determinant_wrong_matrix_dimensions(self):
        print("------ test_determinant_wrong_matrix_dimensions BEGIN : ------")
        matrix_undertest = Matrix([[1, 51, 1], [2, 5, 31]])
        det = matrix_undertest.determinant()
        print("Original matrix : %s " %matrix_undertest)
        print("Result = %s " %det)
        print("------ test_determinant_wrong_matrix_dimensions END. ------\n")
        self.assertEqual(det, None)

    def test_get_columns(self):
        print("------ test_get_columns BEGIN : ------")
        print("Obtain 1st and 3rd column from: ")
        tst_matrix = Matrix([[1, 1, 1], [1, 1, 31], [1, 1, 4], [1,1,1]])
        print(tst_matrix)
        matrix_undertest= tst_matrix.get_column([1,3])
        result_matrix = Matrix([[1, 1], [1, 31], [1, 4] , [1, 1]])
        print("Result = %s" %result_matrix)
        self.assertEqual( matrix_undertest.columns, result_matrix.columns)
        self.assertEqual(matrix_undertest.rows, result_matrix.rows)
        print("------ test_get_columns END. ------\n")

    def test_get_columns_index_out_of_range(self):
        print("------ test_get_columns_index_out_of_range BEGIN : ------")
        print("Obtain 6th column from: ")
        tst_matrix = Matrix([[1, 1, 1], [1, 1, 31], [1, 1, 4], [1,1,1]])
        print(tst_matrix)
        matrix_undertest= tst_matrix.get_column([6])
        print("Result = %s" %matrix_undertest)
        print("------ test_get_columns_index_out_of_range END. ------\n")
        self.assertEqual(matrix_undertest.rows,[])

    def test_get_rows(self):
        print("------ test_get_rows BEGIN : ------")
        tst_matrix = Matrix([[1, 1, 1], [1, 1, 31], [1, 1, 4], [1,1,1]])
        matrix_undertest= tst_matrix.get_rows([1,3])
        result_matrix = Matrix([[1, 1, 1], [1, 1, 4]])
        print("Origin matrix : %s" %tst_matrix)
        print("Get 1st and 3rd row:")
        print("Result = %s" %matrix_undertest)
        self.assertEqual( matrix_undertest.columns, result_matrix.columns)
        self.assertEqual(matrix_undertest.rows, result_matrix.rows)
        print("------ test_get_rows END : ------\n")

    def test_get_rows_out_of_index(self):
        print("------ test_get_rows_out_of_index BEGIN : ------")
        tst_matrix = Matrix([[1, 1, 1], [1, 1, 31], [1, 1, 4], [1,1,1]])
        matrix_undertest= tst_matrix.get_rows([6])
        result_matrix = Matrix([[1, 1, 1], [1, 1, 4]])
        print("Origin matrix : %s" %tst_matrix)
        print("Get 6th row:")
        print("Result = %s" %matrix_undertest)
        print("------ test_get_rows_out_of_index END : ------\n")
        self.assertEqual(matrix_undertest.rows,[])

    def test_getsubmatrix_2x2_successful_index_0_0(self):
        print("------ test_getsubmatrix_2x2_successful_index_0_0 BEGIN : ------")
        tst_matrix = Matrix([[1, 2, 3,4],
                            [4, 5, 6,7],
                            [7, 8, 9,10]])
        result_matrix = Matrix([[1,2],
                                            [4,5]])
        matrix_under_tst = tst_matrix.get_submatrix(dimension_row=2,
                                                    dimension_col=2,
                                                    index_row=0,
                                                    index_col=0)
        print("Original = %s" %tst_matrix)
        print("Obtain a 2x2 matrix, index (0,0) :")
        print("Result = %s" %matrix_under_tst)
        print("------ test_getsubmatrix_successful_index_0_0 END. ------\n")
        self.assertEqual( matrix_under_tst.columns, result_matrix.columns)
        self.assertEqual(matrix_under_tst.rows, result_matrix.rows)

    def test_getsubmatrix_2x2_successful_index_0_1(self):
        print("------ test_getsubmatrix_2x2_successful_index_0_0 BEGIN : ------")
        tst_matrix = Matrix([[1, 2, 3,4],
                            [4, 5, 6,7],
                            [7, 8, 9,10]])
        result_matrix = Matrix([[2,3],
                                            [5,6]])
        matrix_under_tst = tst_matrix.get_submatrix(dimension_row=2,
                                                    dimension_col=2,
                                                    index_row=0,
                                                    index_col=1)
        print("Original = %s" %tst_matrix)
        print("Obtain a 2x2 matrix, index (0,1) :")
        print("Result = %s" %matrix_under_tst)
        print("------ test_getsubmatrix_successful_index_0_1 END. ------\n")
        self.assertEqual( matrix_under_tst.columns, result_matrix.columns)
        self.assertEqual(matrix_under_tst.rows, result_matrix.rows)

    def test_getsubmatrix_2x2_index_out_of_range(self):
        print("------ test_getsubmatrix_2x2_index_out_of_range BEGIN : ------")
        tst_matrix = Matrix([[1, 2, 3,4],
                            [4, 5, 6,7],
                            [7, 8, 9,10]])
        result_matrix = Matrix([[1,2],
                                            [4,5]])
        matrix_under_tst = tst_matrix.get_submatrix(dimension_row=2,
                                                    dimension_col=2,
                                                    index_row=0,
                                                    index_col=5)
        print("Original = %s" %tst_matrix)
        print("Obtain a 2x2 matrix, index (0,5) :")
        print("Result = %s" %matrix_under_tst)
        print("------ test_getsubmatrix_2x2_index_out_of_range END. ------\n")
        self.assertEqual(matrix_under_tst, None)