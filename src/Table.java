import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.List;

public class Table {
    String title;
    List<String> index, columns;
    long[][] values;

    int cur_row = 0, cur_col = 0;

    Table(String title, List<String> index, List<String> columns) {
        this.title = title;
        this.index = index;
        this.columns = columns;
        values = new long[index.size()][columns.size()];
    }

    void set(long value) {
        values[cur_row][cur_col] = value;
        ++cur_col;
        if (cur_col == columns.size()) {
            ++cur_row;
            cur_col = 0;
        }
    }

    public void toTsv(String fileName) {
        try {
            PrintStream outputStream = new PrintStream(new FileOutputStream(fileName));
            outputStream.println(title);
            outputStream.println("\t" + String.join("\t", columns));
            outputStream.println(index.get(0) + "\t" + values[0][0]);
            outputStream.flush();
            outputStream.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}
