import os
import requests

raw_links_dirty ='''
https://frankfurt.apollo.olxcdn.com/v1/files/mn9txntgdpos3-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/fxvyt5l3ghzr-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/w30o99ae10ae-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/uqbv8fhbmtkb1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/v9znhrlegx3f2-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/rp5midgcvmdm-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/osm8tobg3wj83-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/ok954ovezqyv2-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/qc2fd4ba76pv1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/otdu28cjgk2z1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/oe8jxe095sex-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/23xti9j5qi4o2-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/uylfrhubr7r51-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/bpn4new4z0p1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/2cemr5yupx6n3-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/qc9lqtc286rw1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/8kje2szqhyhe-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/fncyzhxm9ujp-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/3tcizqmuva9a1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/z8x70ayzo24p-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/3digf54e8j82-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/s6bpgfstqnc13-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/2ie3k9ovar8u1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/7h7znp67hrm-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/6fotyrd9to8a2-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/ptkmi7kgzksy2-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/mlah0p8jyzol-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/ad5ljio8jrky-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/6ua0nulryfyi-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/kv4iw3afbaj5-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/fdvhhsnt23ug1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/dlzumz3g1o782-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/7hrzqp0eq2mn1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/smpi9ezq5qdw1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/qywzu6b60dtm-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/k0lraawgmx1a1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/as4u6w8kn7gz2-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/m0sxeokk72aj1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/abd84s31b1n12-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/vcb64mdme0qx2-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/7rnfh5xb1fy01-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/xleow0vblbv11-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/hrcwn04vaozn3-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/6vafgde4uuwi-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/74vncrig14dv1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/6jdwhgchos1s-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/t9pj0i7qaquv3-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/p54n7by8epv01-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/t5dqvkbxkv5l1-KZ/image;s=516x361
https://frankfurt.apollo.olxcdn.com/v1/files/8veuh5o5hv5e3-KZ/image;s=516x361
'''

image_links = [line.strip() for line in raw_links_dirty.splitlines() if line.strip()]

save_folder = "dataset/чистота/грязныйдоп"


os.makedirs(save_folder, exist_ok=True)


for i, url in enumerate(image_links, start=676):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        # always save as .webp
        filename = f"dirty_{i}.webp"
        filepath = os.path.join(save_folder, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✅ Saved {filename}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")