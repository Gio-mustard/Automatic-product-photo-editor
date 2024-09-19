from PIL import Image
import numpy as np
import unittest

def get_image_row(image: Image.Image, row_index: int) -> np.ndarray:
    """
    Get a specific row from a PIL Image.

    Args:
    image (PIL.Image.Image): The input PIL Image.
    row_index (int): The row number to retrieve (0-indexed).

    Returns:
    np.ndarray: A numpy array representing the requested row of the image.
    """
    img_array = np.array(image)

    if row_index < 0 or row_index >= img_array.shape[0]:
        raise ValueError(f"Row number {row_index} is out of bounds for image with height {img_array.shape[0]}")

    return img_array[row_index] # row

def get_image_column(image: Image.Image, column_index: int) -> np.ndarray:
    """
    Get a specific column from a PIL Image.

    Args:
    image (PIL.Image.Image): The input PIL Image.
    column_index (int): The row number to retrieve (0-indexed).

    Returns:
    np.ndarray: A numpy array representing the requested row of the image.
    """
    img_array = np.array(image)

    if column_index < 0 or column_index >= img_array.shape[1]:
        raise ValueError(f"Column number {column_index} is out of bounds for image with height {img_array.shape[1]}")

    return img_array[:,column_index] # column


class TestGetImageRow(unittest.TestCase):

    def setUp(self):
        # Create a sample image for testing
        self.test_image = Image.new('RGB', (100, 50), color='red')
        # Add a blue row at index 25
        img_array = np.array(self.test_image)
        img_array[25] = [0, 0, 255]  # Blue
        self.test_image = Image.fromarray(img_array)

    def test_valid_row(self):
        row = get_image_row(self.test_image, 25)
        self.assertEqual(row.shape, (100, 3))
        np.testing.assert_array_equal(row, np.full((100, 3), [0, 0, 255]))

    def test_first_row(self):
        row = get_image_row(self.test_image, 0)
        self.assertEqual(row.shape, (100, 3))
        np.testing.assert_array_equal(row, np.full((100, 3), [255, 0, 0]))

    def test_last_row(self):
        row = get_image_row(self.test_image, 49)
        self.assertEqual(row.shape, (100, 3))
        np.testing.assert_array_equal(row, np.full((100, 3), [255, 0, 0]))

    def test_out_of_bounds_negative(self):
        with self.assertRaises(ValueError):
            get_image_row(self.test_image, -1)

    def test_out_of_bounds_too_large(self):
        with self.assertRaises(ValueError):
            get_image_row(self.test_image, 50)

    def test_grayscale_image(self):
        gray_image = self.test_image.convert('L')
        row = get_image_row(gray_image, 25)
        self.assertEqual(row.shape, (100,))
        # The blue row will be converted to a gray value
        self.assertTrue(np.all(row != 255))  # Not white
        self.assertTrue(np.all(row != 0))    # Not black


if __name__ == '__main__':
    unittest.main()

class TestGetImageColumn(unittest.TestCase):

    def setUp(self):
        # Create a sample image for testing
        self.test_image = Image.new('RGB', (50, 100), color='red')
        # Add a blue column at index 25
        img_array = np.array(self.test_image)
        img_array[:, 25] = [0, 0, 255]  # Blue
        self.test_image = Image.fromarray(img_array)

    def test_valid_column(self):
        column = get_image_column(self.test_image, 25)
        self.assertEqual(column.shape, (100, 3))
        np.testing.assert_array_equal(column, np.full((100, 3), [0, 0, 255]))

    def test_first_column(self):
        column = get_image_column(self.test_image, 0)
        self.assertEqual(column.shape, (100, 3))
        np.testing.assert_array_equal(column, np.full((100, 3), [255, 0, 0]))

    def test_last_column(self):
        column = get_image_column(self.test_image, 49)
        self.assertEqual(column.shape, (100, 3))
        np.testing.assert_array_equal(column, np.full((100, 3), [255, 0, 0]))

    def test_out_of_bounds_negative(self):
        with self.assertRaises(ValueError):
            get_image_column(self.test_image, -1)

    def test_out_of_bounds_too_large(self):
        with self.assertRaises(ValueError):
            get_image_column(self.test_image, 50)

    def test_grayscale_image(self):
        gray_image = self.test_image.convert('L')
        column = get_image_column(gray_image, 25)
        self.assertEqual(column.shape, (100,))
        # The blue column will be converted to a gray value
        self.assertTrue(np.all(column != 255))  # Not white
        self.assertTrue(np.all(column != 0))    # Not black


if __name__ == '__main__':
    unittest.main()