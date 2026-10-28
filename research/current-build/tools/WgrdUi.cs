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
 public static string Capture(string file,int x,int y) { if(String.IsNullOrWhiteSpace(file)) throw new ArgumentException("Output path is required","file"); return CaptureAction(file,x,y,false); }
 public static string CaptureRight(string file,int x,int y) { if(String.IsNullOrWhiteSpace(file)) throw new ArgumentException("Output path is required","file"); return CaptureAction(file,x,y,true); }
 public static string CaptureOnly(string file) { if(String.IsNullOrWhiteSpace(file)) throw new ArgumentException("Output path is required","file"); return CaptureAction(file,-1,-1,false); }
 public static string Click(int x,int y) { if(x<0 || y<0) throw new ArgumentOutOfRangeException("coordinates"); return CaptureAction(null,x,y,false); }
 public static string ClickRight(int x,int y) { if(x<0 || y<0) throw new ArgumentOutOfRangeException("coordinates"); return CaptureAction(null,x,y,true); }
 static string CaptureAction(string file,int x,int y,bool right) {
  if(file!=null && File.Exists(file)) throw new IOException("Refusing overwrite");
  SetProcessDPIAware();
  var ps=Process.GetProcessesByName("WarGame3");
  if(ps.Length!=1) throw new Exception("Expected exactly one game process");
  var h=ps[0].MainWindowHandle;
  if(h==IntPtr.Zero) throw new Exception("No game window");
  ShowWindow(h,9);SetForegroundWindow(h);Thread.Sleep(600);
  if(GetForegroundWindow()!=h) throw new Exception("Game not foreground");
  if(x>=0 && y>=0) {
   int screenWidth=GetSystemMetrics(0),screenHeight=GetSystemMetrics(1);
   if(screenWidth<=0 || screenHeight<=0 || x>=screenWidth || y>=screenHeight) throw new ArgumentOutOfRangeException("coordinates");
   if(!SetCursorPos(x,y)) throw new Exception("Cannot set cursor position");
   if(GetForegroundWindow()!=h) throw new Exception("Game lost foreground before input");
   mouse_event(right?8u:2u,0,0,0,UIntPtr.Zero);Thread.Sleep(70);mouse_event(right?16u:4u,0,0,0,UIntPtr.Zero);
  }
  if(file==null) return "pid="+ps[0].Id+" game="+h+" foreground="+GetForegroundWindow()+" action="+(right?"right":"left")+"_attempted";
  Thread.Sleep(1500);
  int width=GetSystemMetrics(0),height=GetSystemMetrics(1);
  using(var b=new Bitmap(width,height)) {
   using(var g=Graphics.FromImage(b)) g.CopyFromScreen(0,0,0,0,new Size(width,height));
   using(var stream=new FileStream(file,FileMode.CreateNew,FileAccess.Write,FileShare.None)) b.Save(stream,ImageFormat.Png);
  }
  return "pid="+ps[0].Id+" game="+h+" foreground="+GetForegroundWindow()+" image="+width+"x"+height;
 }
}
