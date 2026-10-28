// Task-scoped Windows UI diagnostics. No game memory or settings writes.
using System;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;
public static class WgrdUi {
 [DllImport("user32.dll")] static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] static extern bool ShowWindow(IntPtr h,int cmd);
 [DllImport("user32.dll")] static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")] static extern void mouse_event(uint f,uint x,uint y,uint data,UIntPtr extra);
 [DllImport("user32.dll")] static extern int GetSystemMetrics(int n);
 public static string Capture(string file,int x,int y) {
  if(File.Exists(file)) throw new IOException("Refusing overwrite");
  SetProcessDPIAware();
  var ps=Process.GetProcessesByName("WarGame3");
  if(ps.Length!=1) throw new Exception("Expected exactly one game process");
  var h=ps[0].MainWindowHandle;
  if(h==IntPtr.Zero) throw new Exception("No game window");
  ShowWindow(h,9);SetForegroundWindow(h);Thread.Sleep(600);
  if(GetForegroundWindow()!=h) throw new Exception("Game not foreground");
  if(x>=0 && y>=0) {
   SetCursorPos(x,y);mouse_event(2,0,0,0,UIntPtr.Zero);Thread.Sleep(70);mouse_event(4,0,0,0,UIntPtr.Zero);
  }
  Thread.Sleep(1500);
  int width=GetSystemMetrics(0),height=GetSystemMetrics(1);
  using(var b=new Bitmap(width,height)) {
   using(var g=Graphics.FromImage(b)) g.CopyFromScreen(0,0,0,0,new Size(width,height));
   b.Save(file,ImageFormat.Png);
  }
  return "pid="+ps[0].Id+" game="+h+" foreground="+GetForegroundWindow()+" image="+width+"x"+height;
 }
}
