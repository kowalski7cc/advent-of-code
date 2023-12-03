import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Map;

class Solution {

    static Map<String, String> numbers = new HashMap<>(
            Map.of(
                    "one", "1",
                    "two", "2",
                    "three", "3",
                    "four", "4",
                    "five", "5",
                    "six", "6",
                    "seven", "7",
                    "eight", "8",
                    "nine", "9"));

    public static String numberMapper(String line) {
        var result = new StringBuilder();
        for (int index = 0; index < line.length(); index++) {
            if (Character.isDigit(line.charAt(index))) {
                result.append(line.charAt(index));
                continue;
            }
            for (int length = 3; length <= 5; length++) {
                if (index + length > line.length()) {
                    break;
                }
                var sub = line.substring(index, index + length);
                if (numbers.containsKey(sub)) {
                    result.append(numbers.get(sub));
                    break;
                }
            }
        }
        return result.toString();
    }

    public static String valueMapper(String line) {
        Character first = null;
        Character last = null;

        for (int i = 0; i < line.length(); i++) {
            if (Character.isDigit(line.charAt(i))) {
                first = line.charAt(i);
                break;
            }
        }

        for (int i = line.length() - 1; i >= 0; i--) {
            if (Character.isDigit(line.charAt(i))) {
                last = line.charAt(i);
                break;
            }
        }

        return String.format("%s%s", first, last);
    }

    public static void main(String[] args) throws IOException {
        var lines = Files.readAllLines(new File("input.txt").toPath());
        var result = lines.stream()
                .map(Solution::valueMapper)
                .filter(s -> s.equals("nullnull") == false)
                .mapToInt(Integer::parseInt)
                .sum();
        System.out.println("Part 1: " + result);

        result = lines.stream()
                .map(Solution::numberMapper)
                .map(Solution::valueMapper)
                .mapToInt(Integer::parseInt)
                .sum();
        System.out.println("Part 2: " + result);
    }
}