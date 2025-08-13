import java.awt.*;
import java.awt.event.*;
import java.io.*;
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import javazoom.jl.player.Player;

public class SimpleMusicPlayer extends JFrame {

    private JButton openButton, playButton, pauseButton, stopButton;
    private JLabel statusLabel, fileLabel;
    private JFileChooser fileChooser;
    private File selectedFile;
    private Player player;
    private Thread playThread;
    private boolean isPaused = false;
    private int pauseLocation = 0;
    private int songTotalLength = 0;
    private FileInputStream FIS;
    private BufferedInputStream BIS;

    public SimpleMusicPlayer() {
        super("Simple Music Player");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(400, 200);
        setLayout(new BorderLayout());

        // === Top Panel for File Info ===
        JPanel topPanel = new JPanel(new GridLayout(2, 1));
        fileLabel = new JLabel("No file selected.");
        statusLabel = new JLabel("Status: Idle");
        topPanel.add(fileLabel);
        topPanel.add(statusLabel);

        // === Bottom Panel for Controls ===
        JPanel bottomPanel = new JPanel();
        openButton = new JButton("Open");
        playButton = new JButton("Play");
        pauseButton = new JButton("Pause");
        stopButton = new JButton("Stop");
        playButton.setEnabled(false);
        pauseButton.setEnabled(false);
        stopButton.setEnabled(false);

        bottomPanel.add(openButton);
        bottomPanel.add(playButton);
        bottomPanel.add(pauseButton);
        bottomPanel.add(stopButton);

        add(topPanel, BorderLayout.CENTER);
        add(bottomPanel, BorderLayout.SOUTH);

        // === File Chooser ===
        fileChooser = new JFileChooser();
        fileChooser.setFileFilter(new FileNameExtensionFilter("MP3 Files", "mp3"));

        // === Button Listeners ===
        openButton.addActionListener(e -> openFile());
        playButton.addActionListener(e -> play());
        pauseButton.addActionListener(e -> pause());
        stopButton.addActionListener(e -> stop());

        setVisible(true);
    }

    // Opens a file chooser and loads the selected MP3
    private void openFile() {
        int ret = fileChooser.showOpenDialog(this);
        if (ret == JFileChooser.APPROVE_OPTION) {
            selectedFile = fileChooser.getSelectedFile();
            fileLabel.setText("Loaded: " + selectedFile.getName());
            playButton.setEnabled(true);
            statusLabel.setText("Status: Ready");
        }
    }

    // Plays the selected MP3 file
    private void play() {
        if (selectedFile == null) return;
        stop(); // Stop current playback if any

        try {
            FIS = new FileInputStream(selectedFile);
            BIS = new BufferedInputStream(FIS);
            player = new Player(BIS);

            songTotalLength = FIS.available();
            pauseLocation = 0;
            isPaused = false;

            playThread = new Thread(() -> {
                try {
                    statusLabel.setText("Status: Playing...");
                    playButton.setEnabled(false);
                    pauseButton.setEnabled(true);
                    stopButton.setEnabled(true);
                    player.play();
                    if (!isPaused) {
                        statusLabel.setText("Status: Finished");
                        pauseButton.setEnabled(false);
                        stopButton.setEnabled(false);
                        playButton.setEnabled(true);
                    }
                } catch (Exception ex) {
                    showError("Playback error: " + ex.getMessage());
                }
            });
            playThread.start();
        } catch (Exception ex) {
            showError("Could not play file: " + ex.getMessage());
        }
    }

    // Pauses or resumes playback
    private void pause() {
        if (player == null) return;
        if (!isPaused) {
            try {
                pauseLocation = FIS.available();
                player.close();
                isPaused = true;
                statusLabel.setText("Status: Paused");
                pauseButton.setText("Resume");
            } catch (Exception ex) {
                showError("Error during pause: " + ex.getMessage());
            }
        } else {
            // Resume playback
            try {
                FIS = new FileInputStream(selectedFile);
                BIS = new BufferedInputStream(FIS);
                FIS.skip(songTotalLength - pauseLocation);
                player = new Player(BIS);

                playThread = new Thread(() -> {
                    try {
                        statusLabel.setText("Status: Playing...");
                        player.play();
                        if (!isPaused) {
                            statusLabel.setText("Status: Finished");
                            pauseButton.setEnabled(false);
                            stopButton.setEnabled(false);
                            playButton.setEnabled(true);
                        }
                    } catch (Exception ex) {
                        showError("Playback error: " + ex.getMessage());
                    }
                });
                isPaused = false;
                pauseButton.setText("Pause");
                playThread.start();
            } catch (Exception ex) {
                showError("Resume failed: " + ex.getMessage());
            }
        }
    }

    // Stops playback and resets controls
    private void stop() {
        try {
            if (player != null) {
                player.close();
            }
        } catch (Exception ignore) {}
        isPaused = false;
        pauseButton.setText("Pause");
        statusLabel.setText("Status: Stopped");
        pauseButton.setEnabled(false);
        stopButton.setEnabled(false);
        playButton.setEnabled(true);
    }

    // Utility to show error dialogs
    private void showError(String message) {
        JOptionPane.showMessageDialog(this, message, "Error", JOptionPane.ERROR_MESSAGE);
        statusLabel.setText("Status: Error");
    }

    public static void main(String[] args) {
        // Set look and feel to system default for a better UI experience
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch(Exception ignore) {}
        SwingUtilities.invokeLater(SimpleMusicPlayer::new);
    }
}
