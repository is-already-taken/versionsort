import sys
import string
import re
from operator import itemgetter

class VersionSort():
  
	def extract_versions(self, lines, versionRegEx, buildNumberSep):
		max_fields = 0
		array = []

		for line in lines:
			# extract version (N.M.O-B)
			match = re.search(versionRegEx, line)
			version = match.group(1)

			# get version and build number part (N.M.O, B)
			version_parts = re.split(buildNumberSep, version)
			version_nmo = version_parts[0]
			version_build = version_parts[1]

			# get version number parts (N, M, O)
			version_nmo_parts = re.split('[^0-9]', version_nmo)

			# remember longest version field count
			length = len(version_nmo_parts)
			if length > max_fields:
				max_fields = length

			# store original line and parts in set and add to array
			tupel = (line, version_nmo_parts, int(version_build))
			array.append(tupel)

		return array, max_fields

	def sort(self, lines, versionRegEx, buildNumberSep):
		out_lines = []
		(array, max_fields) = self.extract_versions(lines, versionRegEx, buildNumberSep)
		

		for version in array:
			version_parts = version[1]
			build = version[2]
			version_sum = 0
			length = len(version_parts)

			for i in range(length):
				version_sum = version_sum + (int(version_parts[i]) * (10000 ** (max_fields - i)))

			version_sum = version_sum + build

			tupel = (version[0], version_parts, build, version_sum)
		
			out_lines.append(tupel)


		return map(lambda x: x[0], sorted(out_lines, key=itemgetter(3), reverse=True))


def read_stdin():
	lines = []
	for line in sys.stdin:
		line = line.replace("\n", "")
		lines.append(line)

	return lines

def main():
	version_sort = VersionSort()

	unsorted_lines = read_stdin()
	sorted_lines = version_sort.sort(unsorted_lines, '^.*/([^/]+)$', '-')

	for version in sorted_lines:
		print version

if __name__ == "__main__":
	main()

