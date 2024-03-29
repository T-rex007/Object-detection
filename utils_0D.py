"""
Author: Tyrel Cadogan
email: shaqc777@yahoo.com
Description: helper functions for object detection
"""


def resize(img, size):
    tmp1 = tf.image.resize(img, size)
    return tmp1.numpy().reshape((size[0], size[1],tmp1.shape[-1]))

def normalize(img):
    return img/255

def show_img(img, figsize=None, ax=None):
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return ax

def detect_faces(img):
    detector = MTCNN()
    results = detector.detect_faces(img)
    bb_lst =[]
    for i in results:
        bb_lst.append(i["box"])
    return bb_lst

### Outline
def outline(ax, lw):
    """
    Outline the passed object with a black border
    """
    ax.set_path_effects([patheffects.Stroke(linewidth =lw , foreground = 'black'), patheffects.Normal()])
###Outline
def draw_bb(ax, b):
    """
    Draws a bounding box around the object 
    """
    patch = ax.add_patch(patches.Rectangle(b[:2], *b[-2:], fill=False, edgecolor = 'white', lw = 2))
    outline(patch, 4)
    
def write_txt(ax, xy, txt, sz = 14):
    """
    writes text on  th image
    """
    text = ax.text(xy[0], xy[1], txt, verticalalignment = 'top', color = 'white',fontsize = sz, weight = 'bold')
    outline(text, 1)

def showImgWithAnn(image, annotations):
    """
    Displays the image with the bounding box or boxes
    args: 
        image: image in numpy format
        annotaions: List of tuples containing bounding boxes info and category id
    """
    a= show_img(img)
    for b, c in annotations:
        b = bb_hw(b)
        draw_bb(a, b)
        write_txt(a, b[:2], categ[c])


def feat_distance_cosine(feat1, feat2):
    similarity = np.dot(feat1 / np.linalg.norm(feat1, 2), feat2 / np.linalg.norm(feat2, 2))
    return similarity

def report(results, n_top=3): ### Go through and understand
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")