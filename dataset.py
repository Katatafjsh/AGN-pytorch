from imports import *

def build_train_valid_sets(PATH = Path('data/')):
    """Function to return train and validation sets from eyeglass data."""
    IMG_PATH = PATH/'eyeglasses'
    CSV_PATH = PATH/'files.csv'
    TMP_PATH = PATH/'tmp'
    TMP_PATH.mkdir(exist_ok=True)

    files = PATH.glob('eyeglasses/*.png')

    with CSV_PATH.open('w') as fo:
        for f in files: fo.write(f'{f.relative_to(IMG_PATH)},0\n')

    CSV_PATH = PATH/'files_sample.csv'
    files = PATH.glob('eyeglasses/*.png')

    with CSV_PATH.open('w') as fo:
        for f in files:
            #if np.random.random()<0.1: 
            fo.write(f'{f.relative_to(IMG_PATH)},1\n')

    fnames,y,classes = csv_source('eyeglasses', CSV_PATH, skip_header=True)

    val_idxs = get_cv_idxs(len(fnames))
    ((val_fnames,trn_fnames),(val_y,trn_y)) = split_by_idx(val_idxs, np.array(fnames), y)

    trn = (trn_fnames,trn_y)
    val = (val_fnames,val_y)

    return trn, val


class EyeglassesDataset(Dataset):
    """Eyeglasses dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with labels.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.label = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.label)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.label.iloc[idx, 0])
        image = io.imread(img_name)
        sample = image

        if self.transform:
            sample = self.transform(sample)

        return sample

