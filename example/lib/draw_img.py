def draw_img(display, img, px, py):
    buffer_size = len(display.buffer)
    width = 84
    width_offset = width + px
    # 1つのデータに縦8px分のデータが入っているので、yは48 / 8 == 6区画ある。区画をbyで表現。
    # 8で割り切りない座標が指定されたら、現在の区画と次の区画の両方に書き込む必要があるので
    # シフトする数も用意しておく
    by = py // 8
    y_bitshift = py % 8
    y_bitshift_nextblock = 8 - y_bitshift

    for c,i in enumerate(img):
        # バイト列の場所
        p = width * by + px + c

        # 処理中のx座標が左右にはみ出す場合は読み飛ばす
        if width_offset <= p % width or p % width < px:
            continue

        # 書き込むデータの用意
        # ビットシフトする必要があるときは次の区画のバイト列に
        # シフトされてはみ出したデータを書き込む
        data = i
        if y_bitshift:
            data = data << y_bitshift & 0xff
            p_nextblock = p + width
            # 上下にはみ出していなければ書き込み
            if 0 <= p_nextblock // width and p_nextblock < buffer_size:
                display.buffer[p_nextblock] |= i >> y_bitshift_nextblock

        # 上にはみ出していた場合は読み飛ばす
        if  p // width < 0:
            continue
        # 下にはみ出したらおわり
        if buffer_size <= p:
            break

        # データの書き込み。|=なのは、上書きする必要があるため
        # ビットシフトした場合はdisplay.buffer[p]が0とは限らない
        display.buffer[p] |= data

    # 1pxずつ打つパターン用。遅い。
    # block_size = 8
    # x = 0
    # y = block_size
    # y_block = 0
    # for i in img:
    #    d = '{:08b}'.format(i)
    #    for p in d:
    #        y -= 1
    #        display.pixel(px + x, py + y_block + y, int(p))
    #        if y == 0:
    #            x += 1
    #            y = block_size
    #        if width <= x:
    #            x = 0
    #            y_block += block_size