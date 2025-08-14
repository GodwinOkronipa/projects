import javazoom.jl.player.Player;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class SimpleMusicPlayer {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java SimpleMusicPlayer <mp3_file>");
            return;
        }
        String filename = args[0];
        try (FileInputStream fis = new FileInputStream(filename)) {
            Player player = new Player(fis);
            System.out.println("Playing: " + filename);
            player.play();
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + filename);
        } catch (Exception e) {
            System.out.println("Error playing file: " + e.getMessage());
        }
    }
}
