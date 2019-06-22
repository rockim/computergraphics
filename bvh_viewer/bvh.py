from lib.openbvh import *
gCamAng = 0
gCamHeight = .1
mouse_x = 1
mouse_y = 1
orbit = 0
panning = 0
camera_x = 0
camera_y = 0
panning_zoom = 1
camera_zoom = 1
minus_zoom = 0
angle_v = 0
angle_h = 0
width = 640
height = 640
l = None
drawjoint = 0
drawbvh = None
class BVH(object):
    def __init__(self, root, frame_interval, frame_count):
        self.currentFrame=0
        self.root=root
        self.frame_interval=frame_interval
        self.frame_count=frame_count
    def drawskeleton(self, skeleton):
        glPushMatrix()
        glTranslatef(skeleton.offset[0],skeleton.offset[1],skeleton.offset[2])
        glColor3ub(255,0,0)
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex(0,0,0)
        glEnd()
        for child in skeleton.children:
            glColor3ub(255,255,255)
            # drawbox(skeleton.offset,child.offset)
            glBegin(GL_LINES)
            glVertex(0,0,0)
            glVertex(child.offset)
            glEnd()
            self.drawskeleton(child)
        glPopMatrix()
    def draw(self):
        glColor(1,1,1,1)
        if self.root:
            self.drawJoint(self.root)
    def drawJoint(self, joint):
        glPushMatrix()
        glMultMatrixf(np.dot(joint.getMatrix(self.currentFrame),joint.getOffsetMatrix()))
        glColor3ub(255,0,0)
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex(0,0,0)
        glEnd()

        for child in joint.children:
            # glColor3ub(255,255,255)
            # glBegin(GL_LINES)
            # glVertex(0,0,0)
            # glVertex(child.offset)å
            # # drawbox([0,0,0],child.offset)
            # glEnd()
            glPushMatrix()
            if child.offset[0]>5 or child.offset[1] > 5 or child.offset[2] > 5:
                glScalef(child.offset[0] + 1, child.offset[1] + 1, child.offset[2] + 1)
            if child.offset[0]>1 and child.offset[0]<5 or child.offset[0]>1 and child.offset[0]<5  or child.offset[0]>1 and child.offset[0]<5:
                glScalef(child.offset[0]+0.1, child.offset[1] + 0.1, child.offset[2] + 0.1)
            if child.offset[0]<1 or child.offset[1]<1 or child.offset[2] < 1:
                glScalef(child.offset[0]+0.05, child.offset[1] + 0.05, child.offset[2] + 0.05)
            glPushMatrix()
            drawCube()
            glPopMatrix()
            glPopMatrix()

            self.drawJoint(child)
        glPopMatrix()

    def advanceFrame(self, d):
        self.currentFrame += d
        if self.currentFrame<0:
            self.currentFrame=0
        if self.currentFrame>=self.frame_count:
            self.currentFrame=0


def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    gluPerspective(45,1,1,10)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)
    glTranslatef(camera_x,camera_y,0)
    glRotated(angle_v, 1,0,0)
    glRotated(angle_h, 0,1,0)
    if camera_zoom >= 0:
        glScalef(camera_zoom,camera_zoom,camera_zoom)
    else:
        glScalef(minus_zoom,minus_zoom,minus_zoom)
    # drawFrame()
    drawFlat()
    # drawCube()
    if drawjoint == 1:
        drawbvh.drawskeleton(l.root)
    if drawjoint == 2:
        drawbvh.draw()
        drawbvh.advanceFrame(1)
        
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0,255,0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0,0,255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
def drawCube():
    glBegin(GL_QUADS)
    glColor3ub(255,255,255)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)

    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)

    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)

    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)

    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()
def drawFlat():
    glBegin(GL_LINES)
    glColor3ub(0,255,0)
    for i in range(9):
        if i == 4:
            glColor3ub(255,0,0)
        else:
            glColor3ub(170,170,170)
        glVertex3fv(np.array([-4.,0.,4-i]))
        glVertex3fv(np.array([4.,0.,4-i]))
    for j in range(9):
        if j == 4:
            glColor3ub(0,0,255)
        else:
            glColor3ub(170,170,170)
        glVertex3fv(np.array([4-j,0.,-4.]))
        glVertex3fv(np.array([4-j,0.,4.]))
    glEnd()
def key_callback(window, key, scancode,action, mos):
    global drawjoint
    if action==glfw.PRESS or action == glfw.REPEAT:
        if key==glfw.KEY_SPACE:
            drawjoint = 2

def cursor_callback(window, xpos, ypos):
    global angle_v, angle_h, mouse_x, mouse_y, camera_x, camera_y, camera_zoom, orbit, panning
    if orbit==1:
        if angle_v >= 360:
            angle_v = 0
        elif angle_v <= -360:
            angle_v = 0
        if angle_h >= 360:
            angle_h = 0
        elif angle_h <= -360:
            angle_h = 0
        angle_v += (ypos - mouse_y)*0.3
        angle_h += (xpos - mouse_x)*0.3
        mouse_x = xpos
        mouse_y = ypos
    if panning == 1:
        camera_x += (xpos- mouse_x)/(width/2)
        camera_y -= (ypos- mouse_y)/(height/2)
        mouse_x = xpos
        mouse_y = ypos
def button_callback(window, button, action, mod):
   global mouse_x, mouse_y, orbit, panning
   if button==glfw.MOUSE_BUTTON_LEFT:
       if action==glfw.PRESS:
           (mouse_x, mouse_y) = glfw.get_cursor_pos(window)
           orbit = 1
       elif action==glfw.RELEASE:
           orbit = 0
   if button==glfw.MOUSE_BUTTON_RIGHT:
       if action==glfw.PRESS:
           (mouse_x, mouse_y) = glfw.get_cursor_pos(window)
           panning = 1
       elif action==glfw.RELEASE:
           panning = 0
def scroll_callback(window, xoffset, yoffset):
    global camera_zoom
    if yoffset <0:
        camera_zoom += 0.01
    elif yoffset >0:
        if camera_zoom>=0.01:
            camera_zoom -= 0.01
        if camera_zoom<0.01:
            camera_zoom -= 0.00001

def drop_callback(window, paths):
    global l,drawbvh, drawjoint
    file_name = paths[0].split("/")
    print("File name: ",file_name[-1])
    l = load(paths[0])
    drawbvh=BVH(l.root,l.frame_interval*1000,l.frame_count)
    drawjoint=1
    if drawjoint == 2:
        drawjoint =0

def main():

    if not glfw.init():
        return
    
    window = glfw.create_window(width,height,"test",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_key_callback(window,key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.make_context_current(window)
    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()
        glfw.swap_buffers(window)


    glfw.terminate()

if __name__=="__main__":
    main()
