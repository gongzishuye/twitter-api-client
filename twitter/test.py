import datetime


def string_to_datetime(string):
  """Converts a string to a datetime object.

  Args:
    string: The string to convert.

  Returns:
    A datetime object.
  """

  format_string = "%a %b %d %H:%M:%S %z %Y"
  try:
    return datetime.datetime.strptime(string, format_string)
  except ValueError:
    return None


if __name__ == "__main__":
  string = "Sat Jun 17 12:29:03 +0000 2023"
  datetime_object = string_to_datetime(string)
  print(datetime_object)