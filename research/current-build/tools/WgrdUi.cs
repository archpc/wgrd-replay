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
 [StructLayout(LayoutKind.Sequential)] struct Rect { public int Left,Top,Right,Bottom; }
 [StructLayout(LayoutKind.Sequential)] struct Point { public int X,Y; }
 [StructLayout(LayoutKind.Sequential)] struct MouseInput { public int X,Y; public uint Data,Flags,Time; public UIntPtr Extra; }
 [StructLayout(LayoutKind.Sequential)] struct KeyboardInput { public ushort Vk,Scan; public uint Flags,Time; public UIntPtr Extra; }
 [StructLayout(LayoutKind.Explicit)] struct InputData {
  [FieldOffset(0)] public MouseInput Mouse;
  [FieldOffset(0)] public KeyboardInput Keyboard;
 }
 [StructLayout(LayoutKind.Sequential)] struct Input { public uint Type; public InputData Data; }
 [DllImport("user32.dll",SetLastError=true)] static extern bool GetClientRect(IntPtr h,out Rect rect);
 [DllImport("user32.dll",SetLastError=true)] static extern bool ClientToScreen(IntPtr h,ref Point point);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
 [DllImport("user32.dll",SetLastError=true)] static extern uint SendInput(uint count,Input[] inputs,int size);

 // Input attempts are not gameplay verification. The caller must observe engine state.
 public static string WindowState(int expectedPid) {
  SetProcessDPIAware();
  var h=GameWindow(expectedPid);
  Rect rect;
  if(!GetClientRect(h,out rect)) throw new Exception("Cannot read client rectangle");
  return "pid="+expectedPid+" hwnd="+h+" foreground="+(GetForegroundWindow()==h)+
   " client="+(rect.Right-rect.Left)+"x"+(rect.Bottom-rect.Top);
 }
 static IntPtr GameWindow(int expectedPid) {
  if(expectedPid<=0) throw new ArgumentOutOfRangeException("expectedPid");
  var ps=Process.GetProcessesByName("WarGame3");
  if(ps.Length!=1 || ps[0].Id!=expectedPid) throw new Exception("Game process identity changed");
  var h=ps[0].MainWindowHandle;
  uint pid;
  if(h==IntPtr.Zero || GetWindowThreadProcessId(h,out pid)==0 || pid!=(uint)expectedPid)
   throw new Exception("Game window identity changed");
  return h;
 }
 static void WaitForeground(IntPtr h,int timeoutMs) {
  if(timeoutMs<1 || timeoutMs>5000) throw new ArgumentOutOfRangeException("timeoutMs");
  ShowWindow(h,9);
  SetForegroundWindow(h);
  var watch=Stopwatch.StartNew();
  while(GetForegroundWindow()!=h) {
   if(watch.ElapsedMilliseconds>=timeoutMs) throw new TimeoutException("Game foreground timeout");
   Thread.Sleep(10); // Poll a concrete foreground condition, not a loading delay.
  }
 }
 public static string ClickClient(int expectedPid,int x,int y,int expectedWidth,int expectedHeight,int timeoutMs) {
  if(expectedWidth<=0 || expectedHeight<=0 || x<0 || y<0 || x>=expectedWidth || y>=expectedHeight)
   throw new ArgumentOutOfRangeException("client coordinates");
  SetProcessDPIAware();
  var h=GameWindow(expectedPid);
  WaitForeground(h,timeoutMs);
  Rect rect;
  if(!GetClientRect(h,out rect) || rect.Right-rect.Left!=expectedWidth || rect.Bottom-rect.Top!=expectedHeight)
   throw new Exception("Client geometry changed; recalibration required");
  var point=new Point { X=x,Y=y };
  if(!ClientToScreen(h,ref point) || !SetCursorPos(point.X,point.Y)) throw new Exception("Cannot place cursor");
  if(GameWindow(expectedPid)!=h || GetForegroundWindow()!=h) throw new Exception("Game lost foreground before input");
  var input=new Input[2];
  input[0].Type=0; input[0].Data.Mouse.Flags=2;
  input[1].Type=0; input[1].Data.Mouse.Flags=4;
  if(SendInput(2,input,Marshal.SizeOf(typeof(Input)))!=2) throw new Exception("Incomplete mouse input");
  return "pid="+expectedPid+" hwnd="+h+" client="+x+","+y+" input_attempted=left_click";
 }
 public static string Key(int expectedPid,ushort virtualKey,int timeoutMs) {
  if(virtualKey==0 || virtualKey>254) throw new ArgumentOutOfRangeException("virtualKey");
  var h=GameWindow(expectedPid);
  WaitForeground(h,timeoutMs);
  if(GameWindow(expectedPid)!=h || GetForegroundWindow()!=h) throw new Exception("Game lost foreground before input");
  var input=new Input[2];
  input[0].Type=1; input[0].Data.Keyboard.Vk=virtualKey;
  input[1].Type=1; input[1].Data.Keyboard.Vk=virtualKey; input[1].Data.Keyboard.Flags=2;
  if(SendInput(2,input,Marshal.SizeOf(typeof(Input)))!=2) throw new Exception("Incomplete keyboard input");
  return "pid="+expectedPid+" hwnd="+h+" input_attempted=key_"+virtualKey;
 }
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
