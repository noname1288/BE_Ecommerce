## 1. **Mô hình tổng thể**

Hệ thống gồm các phần chính:

1. **Customer** (quản lý thông tin người dùng, phân loại khách hàng)
2. **Cart** (quản lý giỏ hàng)
3. **Order** (quản lý đơn hàng)
4. **Shipping** (quản lý vận chuyển)
5. **Payment** (quản lý thanh toán)
6. **Items** (quản lý sản phẩm: sách, điện thoại, quần áo, giày dép,…)

Bên cạnh đó, theo đề bài, **Customer** có 4 loại (4 “customer types”) với chức năng riêng:

1. **Guest** (chưa đăng ký, có thể duyệt sản phẩm, thêm giỏ tạm,…)
2. **Registered User** (người dùng đã đăng ký)
3. **VIP User** (người dùng ưu tiên, có thêm các đặc quyền)
4. **Admin** (quản trị, có quyền cao nhất)

Bạn sẽ thể hiện mối quan hệ giữa **loại khách hàng** và **chức năng** của mỗi module thông qua **use case diagram**.

---

## 2. **Chức năng chi tiết**

### 2.1. **Customer Module** (7 chức năng)

1. **Register account**: Tạo tài khoản cho người dùng mới (Guest -> Registered).
2. **Login/Logout**: Đăng nhập, đăng xuất.
3. **Edit profile**: Thay đổi thông tin cá nhân, mật khẩu, ảnh đại diện,…
4. **Manage addresses**: Thêm, xoá, cập nhật địa chỉ giao hàng.
5. **Manage payment info**: Lưu phương thức thanh toán mặc định (thẻ tín dụng, ví điện tử,…).
6. **View purchase history**: Xem lại các đơn hàng đã mua (đối với Registered/VIP).
7. **Deactivate account**: Hủy hoặc vô hiệu hóa tài khoản.

### *Phân quyền ví dụ:*

- **Guest**: Không thể truy cập các tính năng quản lý tài khoản; chỉ có thể **Register**.
- **Registered** & **VIP**: Truy cập tất cả chức năng của Customer Module.
- **Admin**: Có quyền quản lý (tạo/sửa/xóa) tài khoản của người dùng khác.

---

### 2.2. **Cart Module** (7 chức năng)

1. **Add item to cart**: Thêm sản phẩm vào giỏ.
2. **Remove item from cart**: Gỡ sản phẩm khỏi giỏ.
3. **Update item quantity**: Tăng/giảm số lượng sản phẩm trong giỏ.
4. **View cart**: Xem chi tiết giỏ hàng.
5. **Apply discount/promo code**: Áp dụng mã khuyến mãi (nếu có).
6. **Move to Wishlist / Save for later**: Lưu sản phẩm để mua sau.
7. **Empty cart**: Xóa toàn bộ sản phẩm trong giỏ.

### *Phân quyền ví dụ:*

- **Guest** có thể thêm/sp mua tạm thời (session). Nếu đăng ký hoặc đăng nhập sẽ lưu lại.
- **Registered** & **VIP** sẽ có giỏ hàng thường trực, đồng bộ trên nhiều thiết bị.
- **Admin** thường không thao tác giỏ hàng.

---

### 2.3. **Order Module** (7 chức năng)

1. **Create order**: Tạo đơn hàng từ giỏ hàng.
2. **Order confirmation**: Xác nhận đơn hàng (chuyển trạng thái “Pending” -> “Confirmed”).
3. **View order status**: Kiểm tra tình trạng đơn hàng (chuẩn bị, đang giao, hoàn tất,…).
4. **Cancel order**: Hủy đơn (nếu chưa giao hoặc có chính sách hủy).
5. **Return/Refund request**: Yêu cầu trả hàng/hoàn tiền.
6. **Reorder**: Đặt lại các đơn hàng cũ (tiện lợi cho khách thường xuyên mua sản phẩm giống nhau).
7. **Generate invoice**: Tạo hóa đơn (PDF) để lưu trữ hoặc gửi qua email.

### *Phân quyền ví dụ:*

- **Registered/VIP**: Quyền đặt hàng, xem chi tiết đơn hàng của chính họ.
- **Admin**: Có thể quản lý tất cả đơn hàng: điều chỉnh/truy vấn/duyệt/hoàn tiền,…

---

### 2.4. **Shipping Module** (7 chức năng)

1. **Select shipping method**: Chọn nhà vận chuyển (VD: DHL, UPS, VNPost,…).
2. **Calculate shipping fee**: Tính phí giao hàng dựa trên địa chỉ, phương thức, trọng lượng.
3. **Tracking order**: Cập nhật mã vận đơn, theo dõi lộ trình.
4. **Update shipping status**: Cập nhật trạng thái: “In Transit”, “Delivered”,…
5. **Manage shipping addresses**: (kết hợp với Customer module) Xác định địa chỉ giao cụ thể.
6. **Schedule delivery**: Cho phép chọn ngày/giờ giao (nếu dịch vụ hỗ trợ).
7. **Shipping insurance**: Tùy chọn bảo hiểm hàng hóa (nếu giá trị cao).

### *Phân quyền ví dụ:*

- **Registered/VIP**: Lựa chọn hoặc theo dõi đơn hàng của mình.
- **Admin**: Cấu hình phương thức giao hàng, quản lý đối tác vận chuyển, cập nhật chính sách.

---

### 2.5. **Payment Module** (7 chức năng)

1. **Payment methods**: Tích hợp các cổng thanh toán (Credit Card, PayPal, Momo,…).
2. **Process payment**: Xử lý giao dịch thanh toán.
3. **Payment confirmation**: Xác nhận giao dịch thành công và chuyển trạng thái đơn hàng.
4. **Manage refunds**: Hoàn tiền cho khách (kết hợp Order module).
5. **View payment history**: Liệt kê các giao dịch đã thực hiện.
6. **Add/Edit payment info**: Lưu thẻ, tài khoản thanh toán (kết hợp Customer module).
7. **Payment notifications**: Gửi email hoặc thông báo trạng thái (thành công/thất bại).

### *Phân quyền ví dụ:*

- **Registered/VIP**: Thực hiện thanh toán cho đơn hàng của họ.
- **Admin**: Theo dõi/tổng hợp doanh thu, quản lý hoàn tiền, cấu hình cổng thanh toán.

---

### 2.6. **Items Module** (7 chức năng)

1. **Create item listing**: Thêm sản phẩm mới (tên, giá, mô tả, danh mục).
2. **Update item info**: Thay đổi thông tin, giá, hình ảnh,…
3. **Delete item**: Gỡ sản phẩm khỏi kho.
4. **View item**: Xem chi tiết sản phẩm (thông tin, hình ảnh, đánh giá,…).
5. **Categorize item**: Phân loại hàng (sách, điện thoại, quần áo, giày dép,…).
6. **Manage stock**: Theo dõi/điều chỉnh số lượng tồn kho.
7. **Reviews & Ratings**: Cho phép người mua đánh giá, chấm sao.

### *Phân quyền ví dụ:*

- **Guest** & **Registered/VIP**: Chỉ có thể **View item**, **Review** (Registered/VIP).
- **Admin**: Đủ quyền CRUD (tạo, sửa, xóa) sản phẩm, cập nhật kho,…

## 3. **Mô tả vai trò (customer types)**

1. **Guest**
    - Chỉ có thể duyệt sản phẩm (Items module: “View item”), xem thông tin cơ bản.
    - Có giỏ hàng tạm (Cart module).
    - Nếu muốn thanh toán hoặc lưu thông tin, buộc phải *Register* (Customer module).
2. **Registered User**
    - Sau khi đăng ký/đăng nhập, có đầy đủ chức năng của Cart, Order, Payment, Shipping.
    - Có thể xem và sửa thông tin tài khoản (Customer).
    - Có thể đánh giá sản phẩm (Items).
3. **VIP User**
    - Tương tự Registered, nhưng có đặc quyền thêm (giảm giá, miễn phí ship,…) tùy cấu hình.
    - Thường có **loyalty points**, quà tặng,…
4. **Admin**
    - Quyền quản lý cao nhất: CRUD trên mọi module (Customer, Items, Payment, Shipping, Order,…).
    - Có thể phân quyền cho user khác, xử lý yêu cầu hoàn tiền, duyệt đơn hàng, cập nhật kho,…

---

## 4. **Hướng dẫn vẽ Use Case Diagram**

- **Tạo các Actor**:
    - Guest, Registered User, VIP User, Admin (4 loại customer).
- **Tạo các Use Case** tương ứng với mỗi chức năng trong từng module (bạn có thể gom một vài chức năng phụ để biểu diễn gọn trong sơ đồ).
- **Kết nối Actor** với Use Case nào mà họ có thể thực hiện.
- **Chỉ rõ các mối quan hệ** (include, extend) nếu cần:
    - Ví dụ: Use case “Thanh toán” (*Payment*) bao gồm luôn “Xác nhận giao dịch” (include),…

Sau khi hoàn thành use case diagram, bạn có thể tiếp tục xây dựng **Class Diagram**, **Sequence Diagram** hoặc **Activity Diagram** chi tiết hơn để mô tả luồng xử lý từng module trong hệ thống.
