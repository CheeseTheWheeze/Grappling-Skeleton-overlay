using System.Diagnostics;
using System.Text;
using System.Windows.Forms;

static class Program
{
    [STAThread]
    static int Main()
    {
        string baseDir = AppContext.BaseDirectory;
        string runtimeDir = Path.Combine(baseDir, "runtime", "python");
        string pythonExe = Path.Combine(runtimeDir, "python.exe");
        string appDir = Path.Combine(baseDir, "app");
        string dataDir = Path.Combine(baseDir, "FightAI_Data");
        string logsDir = Path.Combine(dataDir, "logs");

        Directory.CreateDirectory(dataDir);
        Directory.CreateDirectory(logsDir);

        string logPath = Path.Combine(
            logsDir,
            $"launcher-{DateTime.Now:yyyyMMdd-HHmmss}.log"
        );

        if (!File.Exists(pythonExe))
        {
            ShowError(
                "Python runtime not found.",
                logPath,
                "Expected runtime at: " + pythonExe
            );
            return 1;
        }

        var startInfo = new ProcessStartInfo
        {
            FileName = pythonExe,
            Arguments = "-m gso_app.entrypoint",
            WorkingDirectory = baseDir,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true,
        };

        startInfo.Environment["PYTHONHOME"] = runtimeDir;
        startInfo.Environment["PYTHONPATH"] = appDir;
        startInfo.Environment["PATH"] = runtimeDir + Path.PathSeparator + Environment.GetEnvironmentVariable("PATH");
        startInfo.Environment["FIGHTAI_DATA_DIR"] = dataDir;
        startInfo.Environment["GSO_DATA_DIR"] = dataDir;
        startInfo.Environment["PYTHONUTF8"] = "1";

        var outputBuilder = new StringBuilder();
        using var process = new Process { StartInfo = startInfo };

        process.OutputDataReceived += (_, args) =>
        {
            if (args.Data != null)
            {
                outputBuilder.AppendLine(args.Data);
            }
        };
        process.ErrorDataReceived += (_, args) =>
        {
            if (args.Data != null)
            {
                outputBuilder.AppendLine(args.Data);
            }
        };

        try
        {
            if (!process.Start())
            {
                ShowError("Failed to start FightAI.", logPath, "Process start returned false.");
                return 1;
            }
        }
        catch (Exception ex)
        {
            ShowError("Failed to launch FightAI.", logPath, ex.ToString());
            return 1;
        }

        process.BeginOutputReadLine();
        process.BeginErrorReadLine();
        process.WaitForExit();

        File.WriteAllText(logPath, outputBuilder.ToString());

        if (process.ExitCode != 0)
        {
            ShowError(
                "FightAI exited with an error.",
                logPath,
                "Exit code: " + process.ExitCode
            );
        }

        return process.ExitCode;
    }

    static void ShowError(string message, string logPath, string details)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(logPath) ?? "");
        File.WriteAllText(logPath, details + Environment.NewLine);
        MessageBox.Show(
            message + Environment.NewLine + "Log: " + logPath,
            "FightAI Launcher",
            MessageBoxButtons.OK,
            MessageBoxIcon.Error
        );
    }
}
