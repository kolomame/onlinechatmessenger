# onlinechatmessenger

クライアントがサーバに接続する形式のチャットメッセンジャーサービス。サーバはバックグラウンドで稼働し、一方でクライアントは CLI を通じてサーバに接続します。接続が確立された後、クライアントはメッセージを入力してサーバに送り、そのメッセージはサーバに接続している他の全てのクライアントにも配信されます。


サーバは CLI で起動し、バックグラウンドで着信接続を待ち受けます。もしサーバがオフラインであれば、それはチャットサービス自体が停止しているということです。

サーバとクライアントは、UDP ネットワークソケットを使ってメッセージのやり取りをします。

メッセージ送信時、サーバとクライアントは一度に最大で 4096 バイトのメッセージを処理します。これは、クライアントが送信できるメッセージの最大サイズです。同じく、最大 4096 バイトのメッセージが他の全クライアントに転送されます。

セッションが開始される際には、クライアントはユーザーにユーザー名を入力させます。

メッセージの送信プロトコルは比較的シンプルです。メッセージの最初の 1 バイト、usernamelen は、ユーザー名の全バイトサイズを示し、これは最大で 255バイト（28 - 1 バイト）になります。サーバはこの初めの usernamelen バイトを読み、送信者のユーザー名を特定します。その後のバイトは送信される実際のメッセージです。この情報はサーバとクライアントによって自由に使用され、ユーザー名の表示や保存が可能です。

サーバにはリレーシステムが組み込まれており、現在接続中のすべてのクライアントの情報を一時的にメモリ上に保存します。新しいメッセージがサーバに届くと、そのメッセージは現在接続中の全クライアントにリレーされます。

クライアントは、しばらくメッセージを送信していない場合、自動的にリレーシステムから削除されます。
